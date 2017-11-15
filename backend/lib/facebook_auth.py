import facebook

from backend.settings import FB_APP_ID
from backend.settings import FB_GRAPH_VERSION


# SCOPES = {'name', 'email', 'picture', 'age_range'}

def facebook_auth_error(uid, token):
    uid = str(uid)
    graph = facebook.GraphAPI(access_token=token, version=FB_GRAPH_VERSION)

    # May throw GraphAPIError for invalid or expired token
    try:
        data = graph.get_object(id='debug_token', input_token=token)['data']
    except Exception as e:
        return str(e)

    if not data.get('is_valid'):
        return 'Data received from Facebook was not valid.'

    if data.get('app_id') != FB_APP_ID:
        return 'Token for wrong application.'

    if data.get('type') != 'USER':
        return 'Not a user token.'
    if data.get('user_id') != uid:
        return 'Token does not belong to user.'

    # scopes = data.get('scopes')
    # if not scopes or not set(scopes) <= SCOPES:
    #     return f'Missing scope: {scopes}'

    return None
