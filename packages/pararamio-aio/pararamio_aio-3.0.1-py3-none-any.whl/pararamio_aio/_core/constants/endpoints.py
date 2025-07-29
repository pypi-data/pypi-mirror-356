"""API endpoint constants."""

__all__ = (
    # Auth endpoints
    'AUTH_INIT_URL',
    'AUTH_LOGIN_URL',
    'AUTH_NEXT_URL',
    'AUTH_TOTP_URL',
    'CHAT_BY_ID_URL',
    # Chat endpoints
    'CHAT_ENDPOINTS',
    'CHAT_LIST_URL',
    'CHAT_POSTS_URL',
    'CHAT_SEND_URL',
    'FILE_DELETE_URL',
    'FILE_DOWNLOAD_URL',
    # File endpoints
    'FILE_UPLOAD_URL',
    'GROUP_BY_ID_URL',
    'GROUP_JOIN_URL',
    'GROUP_LEAVE_URL',
    # Group endpoints
    'GROUP_LIST_URL',
    'POST_BY_ID_URL',
    'POST_CREATE_URL',
    'POST_DELETE_URL',
    # Post endpoints
    'POST_ENDPOINTS',
    'POST_UPDATE_URL',
    'USER_BY_ID_URL',
    # User endpoints
    'USER_PROFILE_URL',
    'USER_SEARCH_URL',
)

# Authentication endpoints
AUTH_INIT_URL = '/auth/init'
AUTH_LOGIN_URL = '/auth/login/password'
AUTH_TOTP_URL = '/auth/totp'
AUTH_NEXT_URL = '/auth/next'

# User endpoints
USER_PROFILE_URL = '/user/profile'
USER_SEARCH_URL = '/user/search'
USER_BY_ID_URL = '/user/{user_id}'

# Chat endpoints
CHAT_LIST_URL = '/chat/list'
CHAT_BY_ID_URL = '/chat/{chat_id}'
CHAT_POSTS_URL = '/chat/{chat_id}/posts'
CHAT_SEND_URL = '/chat/{chat_id}/send'

# Grouped chat endpoints for convenience
CHAT_ENDPOINTS = {
    'list': CHAT_LIST_URL,
    'by_id': CHAT_BY_ID_URL,
    'posts': CHAT_POSTS_URL,
    'send': CHAT_SEND_URL,
}

# Post endpoints
POST_BY_ID_URL = '/post/{post_id}'
POST_CREATE_URL = '/post/create'
POST_UPDATE_URL = '/post/{post_id}/update'
POST_DELETE_URL = '/post/{post_id}/delete'

# Grouped post endpoints for convenience
POST_ENDPOINTS = {
    'by_id': POST_BY_ID_URL,
    'create': POST_CREATE_URL,
    'update': POST_UPDATE_URL,
    'delete': POST_DELETE_URL,
}

# Group endpoints
GROUP_LIST_URL = '/group/list'
GROUP_BY_ID_URL = '/group/{group_id}'
GROUP_JOIN_URL = '/group/{group_id}/join'
GROUP_LEAVE_URL = '/group/{group_id}/leave'

# File endpoints
FILE_UPLOAD_URL = '/upload/{perm}'
FILE_DOWNLOAD_URL = '/download/{guid}/{filename}'
FILE_DELETE_URL = '/delete/{guid}'
