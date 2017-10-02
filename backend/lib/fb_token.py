import time

import facebook

from backend.settings import FB_APP_ID
from backend.settings import FB_GRAPH_VERSION

# TODO: Update scopes to include email, etc.
SCOPES = {'user_friends', 'public_profile'}


def fb_token_is_valid(uid, token):
    uid = str(uid)
    graph = facebook.GraphAPI(access_token=token, version=FB_GRAPH_VERSION)

    # May throw -- GraphAPIError: Invalid OAuth access token.
    try:
        data = graph.get_object(id='debug_token', input_token=token)['data']
    except:
        return False

    if not data.get('is_valid'):
        return False

    if data.get('app_id') != FB_APP_ID:
        return False

    if data.get('type') != 'USER':
        return False
    if data.get('user_id') != uid:
        return False

    expires_at = data.get('expires_at')
    if not expires_at or time.time() > expires_at:
        return False

    scopes = data.get('scopes')
    if not scopes or not set(scopes) <= SCOPES:
        return False

    return True
