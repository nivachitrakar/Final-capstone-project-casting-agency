from functools import wraps
from flask import request
from jose import jwt
import os
import json
from urllib.request import urlopen
from authlib.integrations.flask_client import OAuth

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE')

oauth = OAuth()

auth0 = oauth.register(
    'auth0',
    consumer_key=os.getenv("AUTH0_CLIENT_ID"),
    consumer_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    request_token_params={
        'scope': 'openid profile email',
        'audience': API_AUDIENCE
    },
    base_url=f'https://{AUTH0_DOMAIN}',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f'https://{AUTH0_DOMAIN}/oauth/token',
    authorize_url=f'https://{AUTH0_DOMAIN}/authorize',
)

def init_app(app):
    """Initialize the OAuth extension with the Flask app."""
    oauth.init_app(app)


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer.'
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer token.'
        }, 401)
    
    token = parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            logging.info(f"payload---->>> {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
                logging.info(f'payload------>>> {payload}')
            except AuthError as e:
                abort(e.status_code, description=e.error)

            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return decorated
    return requires_auth_decorator

def requires_role(required_role):
    def requires_role_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = get_token_auth_header()
            payload = jwt.decode(token, urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').read(), algorithms=ALGORITHMS, audience=API_AUDIENCE)
            if 'roles' not in payload or required_role not in payload['roles']:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'Permission not found.'
                }, 403)
            return f(*args, **kwargs)
        return decorated_function
    return requires_role_decorator
