"""Cookie management with versioning, locking and multiple storage backends."""
# pylint: disable=too-many-lines

from __future__ import annotations

import asyncio
import functools
import json
import logging
import os
import threading
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from http.cookiejar import Cookie, CookieJar
from pathlib import Path
from typing import Any, Callable, TypeVar

from .exceptions.base import PararamioException

T = TypeVar('T')


log = logging.getLogger(__name__)


class CookieManager(ABC):
    """Abstract cookie manager with versioning and locking support."""

    @abstractmethod
    def load_cookies(self) -> bool:
        """Load cookies from storage."""

    @abstractmethod
    def save_cookies(self) -> None:
        """Save cookies to storage."""

    @abstractmethod
    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""

    @abstractmethod
    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""

    @abstractmethod
    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""

    @abstractmethod
    def clear_cookies(self) -> None:
        """Clear all cookies."""

    @abstractmethod
    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""

    @abstractmethod
    def acquire_auth_lock(self, timeout: float = 30.0) -> bool:
        """Acquire lock for authentication process."""

    @abstractmethod
    def release_auth_lock(self) -> None:
        """Release authentication lock."""

    @abstractmethod
    def check_version(self) -> bool:
        """Check if our version matches storage version."""

    @abstractmethod
    def refresh_if_needed(self) -> bool:
        """Reload cookies if version changed."""

    @abstractmethod
    def handle_auth_error(self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Handle authentication error with version check and retry."""


class CookieManagerMixin:
    """Mixin with common cookie management functionality."""

    # These attributes are expected to be defined by classes using this mixin
    _cookies: dict[str, Cookie]
    _version: int

    @staticmethod
    def make_key(cookie: Cookie) -> str:
        """Make a unique key for cookie."""
        return f'{cookie.domain}:{cookie.path}:{cookie.name}'

    @staticmethod
    def cookie_to_dict(cookie: Cookie) -> dict[str, Any]:
        """Convert Cookie object to dictionary."""
        return {
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
            'secure': cookie.secure,
            'expires': cookie.expires,
            'discard': cookie.discard,
            'comment': cookie.comment,
            'comment_url': cookie.comment_url,
            'rfc2109': cookie.rfc2109,
            'port': cookie.port,
            'port_specified': cookie.port_specified,
            'domain_specified': cookie.domain_specified,
            'domain_initial_dot': cookie.domain_initial_dot,
            'path_specified': cookie.path_specified,
            'version': cookie.version,
        }

    @staticmethod
    def dict_to_cookie(data: dict[str, Any]) -> Cookie | None:
        """Convert dictionary to Cookie object."""
        try:
            return Cookie(
                version=data.get('version', 0),
                name=data['name'],
                value=data['value'],
                port=data.get('port'),
                port_specified=data.get('port_specified', False),
                domain=data['domain'],
                domain_specified=data.get('domain_specified', True),
                domain_initial_dot=data.get('domain_initial_dot', False),
                path=data['path'],
                path_specified=data.get('path_specified', True),
                secure=data.get('secure', False),
                expires=data.get('expires'),
                discard=data.get('discard', False),
                comment=data.get('comment'),
                comment_url=data.get('comment_url'),
                rest={},
                rfc2109=data.get('rfc2109', False),
            )
        except (KeyError, TypeError):
            log.exception('Failed to create cookie from dict')
            return None

    def populate_jar(self, cookie_jar: CookieJar) -> None:
        """Populate a CookieJar with our cookies."""
        cookies = getattr(self, '_cookies', {})
        # Check if we need thread safety
        lock = getattr(self, '_lock', None)
        if lock is not None:
            with lock:
                for cookie in cookies.values():
                    cookie_jar.set_cookie(cookie)
        else:
            for cookie in cookies.values():
                cookie_jar.set_cookie(cookie)

    def has_cookies(self) -> bool:
        """Check if manager has any cookies."""
        return bool(getattr(self, '_cookies', {}))

    def _get_file_version(self) -> int:
        """Get current version from file."""
        version_path = getattr(self, 'version_path', None)
        if not version_path or not version_path.exists():
            return 0

        try:
            with version_path.open(encoding='utf-8') as f:
                return int(f.read().strip())
        except (OSError, ValueError):
            return 0

    def _load_cookies_from_json(self, data: str | None) -> bool:
        """Load cookies from JSON data.

        Args:
            data: JSON string containing cookies data

        Returns:
            True if loaded successfully, False otherwise
        """
        if not data:
            return False

        parsed_data = json.loads(data)
        return self._load_cookies_from_dict(parsed_data)

    def _load_cookies_from_dict(self, data: dict) -> bool:
        """Load cookies from dictionary data.

        Args:
            data: Dictionary containing cookies data

        Returns:
            True if loaded successfully
        """
        self._version = data.get('version', 0)
        cookies_data = data.get('cookies', [])

        self._cookies.clear()
        for cookie_dict in cookies_data:
            cookie = self.dict_to_cookie(cookie_dict)
            if cookie:
                key = self.make_key(cookie)
                self._cookies[key] = cookie

        return True

    def _prepare_cookies_data(self) -> dict:
        """Prepare cookies data for saving.

        Returns:
            Dictionary with version, cookies, and timestamp
        """
        cookies = getattr(self, '_cookies', {})
        version = getattr(self, '_version', 0)

        cookies_data = [
            self.cookie_to_dict(cookie)
            for cookie in cookies.values()
            if not cookie.discard  # Only save persistent cookies
        ]

        return {
            'version': version,
            'cookies': cookies_data,
            'saved_at': datetime.now(timezone.utc).isoformat(),
        }

    def _increment_file_version(self) -> int:
        """Increment version and save to file."""
        version_path = getattr(self, 'version_path', None)
        if not version_path:
            return 0

        self._version = self._get_file_version() + 1

        try:
            version_path.parent.mkdir(parents=True, exist_ok=True)
            with version_path.open('w', encoding='utf-8') as f:
                f.write(str(self._version))
        except OSError:
            log.exception('Failed to save version')

        return self._version


class FileCookieManager(CookieManagerMixin, CookieManager):
    """File-based cookie manager implementation."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.lock_path = Path(f'{file_path}.lock')
        self.version_path = Path(f'{file_path}.version')
        self._cookies: dict[str, Cookie] = {}
        self._version: int = 0
        self._lock = threading.Lock()
        self._lock_fd: int | None = None

        # Automatically load cookies if file exists
        if self.file_path.exists():
            try:
                self.load_cookies()
            except (OSError, json.JSONDecodeError, ValueError):
                # Log error but don't fail initialization
                log.exception(
                    'Failed to load cookies from %s during initialization', self.file_path
                )

    @property
    def version(self) -> int:
        """Get current version."""
        return self._version

    def load_cookies(self) -> bool:
        """Load cookies from file."""
        with self._lock:
            if not self.file_path.exists():
                return False

            try:
                with self.file_path.open(encoding='utf-8') as f:
                    data = json.load(f)

                self._load_cookies_from_dict(data)

            except (OSError, json.JSONDecodeError) as e:
                log.warning('Failed to load cookies from %s: %s', self.file_path, e)
                return False
            return True

    def save_cookies(self) -> None:
        """Save cookies to file."""
        with self._lock:
            data = self._prepare_cookies_data()

            # Ensure directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temp file first
            temp_path = Path(f'{self.file_path}.tmp')
            try:
                with temp_path.open('w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                # Atomic rename
                temp_path.rename(self.file_path)
            except (OSError, TypeError, ValueError):
                log.exception('Failed to save cookies to %s', self.file_path)
                if temp_path.exists():
                    temp_path.unlink()
                raise

    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""
        with self._lock:
            key = self.make_key(cookie)
            self._cookies[key] = cookie
            self._version = self._increment_version()

    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""
        with self._lock:
            key = f'{domain}:{path}:{name}'
            return self._cookies.get(key)

    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""
        with self._lock:
            return list(self._cookies.values())

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        with self._lock:
            self._cookies.clear()
            self._version = self._increment_version()

    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""
        with self._lock:
            for cookie in cookie_jar:
                key = self.make_key(cookie)
                self._cookies[key] = cookie
            self._version = self._increment_version()

    def acquire_auth_lock(self, timeout: float = 30.0) -> bool:
        """Acquire file lock with timeout."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Try to create lock file exclusively
                self._lock_fd = os.open(
                    str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
                )
            except FileExistsError:
                # Lock exists, check if it's stale
                if self._is_lock_stale():
                    self._remove_stale_lock()
                    continue
                time.sleep(0.1)
                continue
            # Write PID for debugging
            os.write(self._lock_fd, str(os.getpid()).encode())
            return True

        return False

    def release_auth_lock(self) -> None:
        """Release file lock."""
        if self._lock_fd is not None:
            try:
                os.close(self._lock_fd)
                self.lock_path.unlink(missing_ok=True)
            except OSError as e:
                log.warning('Failed to release lock: %s', e)
            finally:
                self._lock_fd = None

    def check_version(self) -> bool:
        """Check if our version matches file version."""
        current_version = self._get_file_version()
        return current_version == self._version

    def refresh_if_needed(self) -> bool:
        """Reload cookies if version changed."""
        if not self.check_version():
            log.info('Cookie version mismatch, reloading...')
            return self.load_cookies()
        return True

    def handle_auth_error(self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Handle authentication error with version check and retry.

        Args:
            retry_callback: Function to call for retry
            *args, **kwargs: Arguments to pass to retry_callback

        Returns:
            Result of retry_callback if successful

        Raises:
            Original exception if all retries fail
        """
        log.info('Authentication error occurred, checking cookie version...')

        # First, check if our cookies are outdated
        if not self.check_version():
            log.info('Cookie version outdated, reloading...')
            if self.load_cookies():
                log.info('Cookies reloaded, retrying with updated cookies...')
                try:
                    return retry_callback(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    log.warning('Retry with updated cookies failed: %s', e)
            else:
                log.warning('Failed to reload cookies')

        # If still failing, acquire lock and re-authenticate
        log.info('Attempting re-authentication...')
        if self.acquire_auth_lock(timeout=30.0):
            try:
                # Clear existing cookies
                self.clear_cookies()
                self.save_cookies()

                # Call retry which should trigger re-authentication
                result = retry_callback(*args, **kwargs)

                # Save new cookies after successful auth
                self.save_cookies()
                return result

            finally:
                self.release_auth_lock()
        msg = 'Failed to acquire authentication lock for re-authentication'
        raise PararamioException(msg)

    def _increment_version(self) -> int:
        """Increment version and save to file."""
        return self._increment_file_version()

    def _is_lock_stale(self, max_age: float = 300.0) -> bool:
        """Check if lock file is stale (older than max_age seconds)."""
        try:
            stat = self.lock_path.stat()
        except FileNotFoundError:
            return False
        age = time.time() - stat.st_mtime
        return age > max_age

    def _remove_stale_lock(self) -> None:
        """Remove stale lock file."""
        try:
            self.lock_path.unlink()
            log.info('Removed stale lock file: %s', self.lock_path)
        except FileNotFoundError:
            pass


class RedisCookieManager(CookieManagerMixin, CookieManager):
    """Redis-based cookie manager implementation."""

    def __init__(self, redis_client: Any, key_prefix: str = 'pararamio:cookies'):
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.data_key = f'{key_prefix}:data'
        self.lock_key = f'{key_prefix}:lock'
        self.version_key = f'{key_prefix}:version'
        self._cookies: dict[str, Cookie] = {}
        self._version: int = 0
        self._lock = threading.Lock()
        self._lock_token: str | None = None

    @property
    def version(self) -> int:
        """Get current version."""
        return self._version

    def load_cookies(self) -> bool:
        """Load cookies from Redis."""
        with self._lock:
            try:
                data = self.redis.get(self.data_key)
                return self._load_cookies_from_json(data)
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
                log.warning('Failed to load cookies from Redis: %s', e)
                return False

    def save_cookies(self) -> None:
        """Save cookies to Redis."""
        with self._lock:
            data = self._prepare_cookies_data()

            try:
                self.redis.set(self.data_key, json.dumps(data))
            except (OSError, TypeError, ValueError, AttributeError):
                log.exception('Failed to save cookies to Redis')
                raise

    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""
        with self._lock:
            key = self.make_key(cookie)
            self._cookies[key] = cookie
            self._version = self._increment_version()

    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""
        with self._lock:
            key = f'{domain}:{path}:{name}'
            return self._cookies.get(key)

    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""
        with self._lock:
            return list(self._cookies.values())

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        with self._lock:
            self._cookies.clear()
            self._version = self._increment_version()

    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""
        with self._lock:
            for cookie in cookie_jar:
                key = self.make_key(cookie)
                self._cookies[key] = cookie
            self._version = self._increment_version()

    def acquire_auth_lock(self, timeout: float = 30.0) -> bool:
        """Acquire distributed lock using Redis."""
        self._lock_token = str(uuid.uuid4())

        start_time = time.time()
        while time.time() - start_time < timeout:
            # Try to set lock with expiration
            if self.redis.set(self.lock_key, self._lock_token, nx=True, ex=300):
                return True
            time.sleep(0.1)

        return False

    def release_auth_lock(self) -> None:
        """Release distributed lock."""
        if self._lock_token:
            # Use Lua script for atomic check-and-delete
            lua_script = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
            """
            try:
                self.redis.eval(lua_script, 1, self.lock_key, self._lock_token)
            except (AttributeError, KeyError) as e:
                log.warning('Failed to release Redis lock: %s', e)
            finally:
                self._lock_token = None

    def check_version(self) -> bool:
        """Check if our version matches Redis version."""
        try:
            version = self.redis.get(self.version_key)
        except (ValueError, AttributeError, TypeError, KeyError):
            return True
        current_version = int(version) if version else 0
        return current_version == self._version

    def refresh_if_needed(self) -> bool:
        """Reload cookies if version changed."""
        if not self.check_version():
            log.info('Cookie version mismatch, reloading...')
            return self.load_cookies()
        return True

    def handle_auth_error(self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Handle authentication error with version check and retry."""
        log.info('Authentication error occurred (Redis), checking cookie version...')

        # First, check if our cookies are outdated
        if not self.check_version():
            log.info('Cookie version outdated, reloading from Redis...')
            if self.load_cookies():
                log.info('Cookies reloaded, retrying with updated cookies...')
                try:
                    return retry_callback(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    log.warning('Retry with updated cookies failed: %s', e)
            else:
                log.warning('Failed to reload cookies from Redis')

        # If still failing, acquire distributed lock and re-authenticate
        log.info('Attempting re-authentication with distributed lock...')
        if self.acquire_auth_lock(timeout=30.0):
            try:
                # Clear existing cookies
                self.clear_cookies()
                self.save_cookies()

                # Call retry which should trigger re-authentication
                result = retry_callback(*args, **kwargs)

                # Save new cookies after successful auth
                self.save_cookies()
                return result

            finally:
                self.release_auth_lock()
        else:
            msg = 'Failed to acquire distributed lock for re-authentication'
            raise PararamioException(msg)

    def _increment_version(self) -> int:
        """Atomically increment version in Redis."""
        try:
            self._version = self.redis.incr(self.version_key)
        except (AttributeError, TypeError):
            log.exception('Failed to increment version in Redis')
            return self._version
        return self._version


class InMemoryCookieManager(CookieManagerMixin, CookieManager):
    """In-memory cookie manager implementation (no persistence)."""

    def __init__(self):
        self._cookies: dict[str, Cookie] = {}
        self._version: int = 0
        self._lock = threading.Lock()

    @property
    def version(self) -> int:
        """Get current version."""
        return self._version

    def load_cookies(self) -> bool:
        """No-op for in-memory manager."""
        # Cookies are already in memory
        return bool(self._cookies)

    def save_cookies(self) -> None:
        """No-op for in-memory manager."""
        # Cookies are already in memory, nothing to save

    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""
        with self._lock:
            key = self.make_key(cookie)
            self._cookies[key] = cookie
            self._version += 1

    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""
        with self._lock:
            key = f'{domain}:{path}:{name}'
            return self._cookies.get(key)

    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""
        with self._lock:
            return list(self._cookies.values())

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        with self._lock:
            self._cookies.clear()
            self._version += 1

    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""
        with self._lock:
            for cookie in cookie_jar:
                key = self.make_key(cookie)
                self._cookies[key] = cookie
            self._version += 1

    def acquire_auth_lock(self, timeout: float = 30.0) -> bool:  # noqa: ARG002
        """Always returns True for in-memory manager."""
        return True

    def release_auth_lock(self) -> None:
        """No-op for in-memory manager."""

    def check_version(self) -> bool:
        """Always returns True for in-memory manager."""
        return True

    def refresh_if_needed(self) -> bool:
        """No-op for in-memory manager."""
        return True

    def handle_auth_error(self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Handle authentication error by retrying."""
        log.info('Authentication error occurred (in-memory), retrying...')

        # For in-memory, just clear cookies and retry
        self.clear_cookies()

        try:
            return retry_callback(*args, **kwargs)
        except (AttributeError, TypeError):
            log.exception('Retry failed')
            raise


# Async versions
class AsyncCookieManager(ABC):
    """Abstract async cookie manager."""

    @abstractmethod
    async def load_cookies(self) -> bool:
        """Load cookies from storage asynchronously."""

    @abstractmethod
    async def save_cookies(self) -> None:
        """Save cookies to storage asynchronously."""

    @abstractmethod
    async def acquire_auth_lock(self, timeout: float = 30.0) -> bool:
        """Acquire lock for authentication process asynchronously."""

    @abstractmethod
    async def release_auth_lock(self) -> None:
        """Release authentication lock asynchronously."""

    @abstractmethod
    async def handle_auth_error(
        self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Handle authentication error with version check and retry asynchronously."""


class AsyncFileCookieManager(CookieManagerMixin, AsyncCookieManager):
    """Async file-based cookie manager."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.lock_path = Path(f'{file_path}.lock')
        self.version_path = Path(f'{file_path}.version')
        self._cookies: dict[str, Cookie] = {}
        self._version: int = 0
        self._lock = asyncio.Lock()
        self._lock_fd: int | None = None

        # Automatically load cookies synchronously if file exists
        if self.file_path.exists():
            try:
                # Use synchronous file reading for initialization
                with self.file_path.open(encoding='utf-8') as f:
                    data = json.load(f)
                self._load_cookies_from_dict(data)
                # Try to load version
                if self.version_path.exists():
                    with self.version_path.open(encoding='utf-8') as f:
                        self._version = int(f.read().strip())
            except (OSError, json.JSONDecodeError, ValueError):
                # Log error but don't fail initialization
                log.exception(
                    'Failed to load cookies from %s during initialization', self.file_path
                )

    @property
    def version(self) -> int:
        """Get current version."""
        return self._version

    async def load_cookies(self) -> bool:
        """Load cookies from file asynchronously."""
        async with self._lock:
            if not self.file_path.exists():
                return False

            try:
                loop = asyncio.get_event_loop()
                read_func = functools.partial(self.file_path.read_text, encoding='utf-8')
                content = await loop.run_in_executor(None, read_func)
                data = json.loads(content)

                self._load_cookies_from_dict(data)

            except (OSError, json.JSONDecodeError) as e:
                log.warning('Failed to load cookies from %s: %s', self.file_path, e)
                return False
            return True

    async def save_cookies(self) -> None:
        """Save cookies to file asynchronously."""
        async with self._lock:
            data = self._prepare_cookies_data()

            # Ensure directory exists
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temp file first
            temp_path = Path(f'{self.file_path}.tmp')
            try:
                loop = asyncio.get_event_loop()
                content = json.dumps(data, indent=2)
                # Use functools.partial to bind the arguments
                write_func = functools.partial(temp_path.write_text, content, encoding='utf-8')
                await loop.run_in_executor(None, write_func)
                # Atomic rename
                await loop.run_in_executor(None, temp_path.rename, self.file_path)
            except (OSError, TypeError, ValueError):
                log.exception('Failed to save cookies to %s', self.file_path)
                if temp_path.exists():
                    temp_path.unlink()
                raise

    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""
        key = self.make_key(cookie)
        self._cookies[key] = cookie
        self._version = self._increment_version()

    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""
        key = f'{domain}:{path}:{name}'
        return self._cookies.get(key)

    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""
        return list(self._cookies.values())

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        self._cookies.clear()
        self._version = self._increment_version()

    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""
        for cookie in cookie_jar:
            key = self.make_key(cookie)
            self._cookies[key] = cookie
        self._version = self._increment_version()

    async def acquire_auth_lock(self, timeout: float = 30.0) -> bool:
        """Acquire file lock asynchronously."""
        start_time = time.time()
        loop = asyncio.get_event_loop()

        while time.time() - start_time < timeout:
            try:
                # Try to create lock file exclusively
                self._lock_fd = await loop.run_in_executor(
                    None, os.open, str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644
                )
            except FileExistsError:
                # Lock exists, check if it's stale
                if await self._is_lock_stale():
                    await self._remove_stale_lock()
                    continue
                await asyncio.sleep(0.1)
                continue
            # Write PID for debugging
            await loop.run_in_executor(None, os.write, self._lock_fd, str(os.getpid()).encode())
            return True

        return False

    async def release_auth_lock(self) -> None:
        """Release file lock asynchronously."""
        if self._lock_fd is not None:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, os.close, self._lock_fd)
                self.lock_path.unlink(missing_ok=True)
            except OSError as e:
                log.warning('Failed to release lock: %s', e)
            finally:
                self._lock_fd = None

    def check_version(self) -> bool:
        """Check if our version matches file version."""
        current_version = self._get_file_version()
        return current_version == self._version

    def refresh_if_needed(self) -> bool:
        """Reload cookies if version changed."""
        # This needs to be async but is called from sync context
        # For now, return False to indicate async operation needed
        return not self.check_version()

    async def refresh_if_needed_async(self) -> bool:
        """Reload cookies if version changed (async version)."""
        if not self.check_version():
            log.info('Cookie version mismatch, reloading...')
            return await self.load_cookies()
        return True

    async def handle_auth_error(
        self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Handle authentication error with version check and retry asynchronously."""
        log.info('Authentication error occurred (async), checking cookie version...')

        # First, check if our cookies are outdated
        if not self.check_version():
            log.info('Cookie version outdated, reloading...')
            if await self.load_cookies():
                log.info('Cookies reloaded, retrying with updated cookies...')
                try:
                    return await retry_callback(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    log.warning('Retry with updated cookies failed: %s', e)
            else:
                log.warning('Failed to reload cookies')

        # If still failing, acquire lock and re-authenticate
        log.info('Attempting re-authentication...')
        if await self.acquire_auth_lock(timeout=30.0):
            try:
                # Clear existing cookies
                self.clear_cookies()
                await self.save_cookies()

                # Call retry which should trigger re-authentication
                result = await retry_callback(*args, **kwargs)

                # Save new cookies after successful auth
                await self.save_cookies()
                return result

            finally:
                await self.release_auth_lock()
        msg = 'Failed to acquire authentication lock for re-authentication'
        raise PararamioException(msg)

    def _increment_version(self) -> int:
        """Increment version and save to file."""
        return self._increment_file_version()

    async def _is_lock_stale(self, max_age: float = 300.0) -> bool:
        """Check if lock file is stale (older than max_age seconds)."""
        try:
            stat = self.lock_path.stat()
        except FileNotFoundError:
            return False
        age = time.time() - stat.st_mtime
        return age > max_age

    async def _remove_stale_lock(self) -> None:
        """Remove stale lock file."""
        try:
            self.lock_path.unlink()
            log.info('Removed stale lock file: %s', self.lock_path)
        except FileNotFoundError:
            pass


class AsyncRedisCookieManager(CookieManagerMixin, AsyncCookieManager):
    """Async Redis-based cookie manager."""

    def __init__(self, redis_client: Any, key_prefix: str = 'pararamio:cookies'):
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.data_key = f'{key_prefix}:data'
        self.lock_key = f'{key_prefix}:lock'
        self.version_key = f'{key_prefix}:version'
        self._cookies: dict[str, Cookie] = {}
        self._version: int = 0
        self._lock = asyncio.Lock()
        self._lock_token: str | None = None

    @property
    def version(self) -> int:
        """Get current version."""
        return self._version

    async def load_cookies(self) -> bool:
        """Load cookies from Redis asynchronously."""
        async with self._lock:
            # Assuming redis_client is async
            try:
                data = await self.redis.get(self.data_key)
                return self._load_cookies_from_json(data)
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
                log.warning('Failed to load cookies from Redis: %s', e)
                return False

    async def save_cookies(self) -> None:
        """Save cookies to Redis asynchronously."""
        async with self._lock:
            data = self._prepare_cookies_data()

            try:
                await self.redis.set(self.data_key, json.dumps(data))
            except (OSError, TypeError, ValueError, AttributeError):
                log.exception('Failed to save cookies to Redis')
                raise

    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""
        key = self.make_key(cookie)
        self._cookies[key] = cookie
        self._version = self._increment_version()

    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""
        key = f'{domain}:{path}:{name}'
        return self._cookies.get(key)

    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""
        return list(self._cookies.values())

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        self._cookies.clear()
        self._version = self._increment_version()

    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""
        for cookie in cookie_jar:
            key = self.make_key(cookie)
            self._cookies[key] = cookie
        self._version = self._increment_version()

    def check_version(self) -> bool:
        """Check if our version matches Redis version."""
        try:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(self.redis.get(self.version_key))
            version = loop.run_until_complete(future)
        except (ValueError, AttributeError, RuntimeError):
            return True
        current_version = int(version) if version else 0
        return current_version == self._version

    async def check_version_async(self) -> bool:
        """Check if our version matches Redis version (async version)."""
        try:
            version = await self.redis.get(self.version_key)
        except (ValueError, AttributeError):
            return True
        current_version = int(version) if version else 0
        return current_version == self._version

    def refresh_if_needed(self) -> bool:
        """Reload cookies if version changed."""
        # This needs to be async
        return not self.check_version()

    async def refresh_if_needed_async(self) -> bool:
        """Reload cookies if version changed (async version)."""
        if not await self.check_version_async():
            log.info('Cookie version mismatch, reloading...')
            return await self.load_cookies()
        return True

    def _increment_version(self) -> int:
        """Atomically increment version in Redis."""
        # This is sync but needs to use async redis
        # For now just increment locally
        self._version += 1
        return self._version

    async def _increment_version_async(self) -> int:
        """Atomically increment version in Redis."""
        try:
            self._version = await self.redis.incr(self.version_key)
        except (AttributeError, TypeError):
            log.exception('Failed to increment version in Redis')
            return self._version
        return self._version

    async def acquire_auth_lock(self, timeout: float = 30.0) -> bool:
        """Acquire distributed lock asynchronously."""
        self._lock_token = str(uuid.uuid4())

        start_time = time.time()
        while time.time() - start_time < timeout:
            # Try to set lock with expiration
            if await self.redis.set(self.lock_key, self._lock_token, nx=True, ex=300):
                return True
            await asyncio.sleep(0.1)

        return False

    async def release_auth_lock(self) -> None:
        """Release distributed lock asynchronously."""
        if self._lock_token:
            lua_script = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
            """
            try:
                await self.redis.eval(lua_script, 1, self.lock_key, self._lock_token)
            except (AttributeError, KeyError) as e:
                log.warning('Failed to release Redis lock: %s', e)
            finally:
                self._lock_token = None

    async def handle_auth_error(
        self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Handle authentication error with version check and retry asynchronously."""
        log.info('Authentication error occurred (async Redis), checking cookie version...')

        # First, check if our cookies are outdated
        if not await self.check_version_async():
            log.info('Cookie version outdated, reloading from Redis...')
            if await self.load_cookies():
                log.info('Cookies reloaded, retrying with updated cookies...')
                try:
                    return await retry_callback(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    log.warning('Retry with updated cookies failed: %s', e)
            else:
                log.warning('Failed to reload cookies from Redis')

        # If still failing, acquire distributed lock and re-authenticate
        log.info('Attempting re-authentication with distributed lock...')
        if await self.acquire_auth_lock(timeout=30.0):
            try:
                # Clear existing cookies
                self.clear_cookies()
                await self.save_cookies()

                # Call retry which should trigger re-authentication
                result = await retry_callback(*args, **kwargs)

                # Save new cookies after successful auth
                await self.save_cookies()
                return result

            finally:
                await self.release_auth_lock()
        msg = 'Failed to acquire distributed lock for re-authentication'
        raise PararamioException(msg)


class AsyncInMemoryCookieManager(CookieManagerMixin, AsyncCookieManager):
    """Async in-memory cookie manager."""

    def __init__(self):
        self._cookies: dict[str, Cookie] = {}
        self._version: int = 0
        self._lock = asyncio.Lock()

    @property
    def version(self) -> int:
        """Get current version."""
        return self._version

    async def load_cookies(self) -> bool:
        """No-op for in-memory manager."""
        async with self._lock:
            return bool(self._cookies)

    async def save_cookies(self) -> None:
        """No-op for in-memory manager."""

    def add_cookie(self, cookie: Cookie) -> None:
        """Add or update a cookie."""
        key = self.make_key(cookie)
        self._cookies[key] = cookie
        self._version += 1

    def get_cookie(self, domain: str, path: str, name: str) -> Cookie | None:
        """Get a specific cookie."""
        key = f'{domain}:{path}:{name}'
        return self._cookies.get(key)

    def get_all_cookies(self) -> list[Cookie]:
        """Get all cookies."""
        return list(self._cookies.values())

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        self._cookies.clear()
        self._version += 1

    def update_from_jar(self, cookie_jar: CookieJar) -> None:
        """Update cookies from a CookieJar."""
        for cookie in cookie_jar:
            key = self.make_key(cookie)
            self._cookies[key] = cookie
        self._version += 1

    def populate_jar(self, cookie_jar: CookieJar) -> None:
        """Populate a CookieJar with stored cookies (synchronous version for async manager)."""
        # Since this is called synchronously, we can't use the async lock
        # Just iterate over cookies without locking
        for cookie in self._cookies.values():
            cookie_jar.set_cookie(cookie)

    # noinspection PyMethodMayBeStatic
    def check_version(self) -> bool:
        """Always returns True for in-memory manager."""
        return True

    # noinspection PyMethodMayBeStatic
    def refresh_if_needed(self) -> bool:
        """No-op for in-memory manager."""
        return True

    async def acquire_auth_lock(self, timeout: float = 30.0) -> bool:  # noqa: ARG002
        """Always returns True for in-memory manager."""
        return True

    async def release_auth_lock(self) -> None:
        """No-op for in-memory manager."""

    async def handle_auth_error(
        self, retry_callback: Callable[..., T], *args: Any, **kwargs: Any
    ) -> T:
        """Handle authentication error by retrying."""
        log.info('Authentication error occurred (async in-memory), retrying...')

        # For in-memory, just clear cookies and retry
        async with self._lock:
            self.clear_cookies()

        try:
            return await retry_callback(*args, **kwargs)
        except (AttributeError, TypeError):
            log.exception('Retry failed')
            raise
