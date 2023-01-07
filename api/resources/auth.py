from functools import wraps
from flask import request
from flask_restful import abort
import jwt
import os
from datetime import datetime, timezone
import calendar

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class AuthorizedTasks:
    def __init__(self):
        self.list = {}
        self.auth_data = {}
    def register_task(self, func):
        self.list[func.__name__]={"func": func}
        self.auth_data[func.__name__]={"func": func}

authorizedTasks = AuthorizedTasks()

def authorized_task(task_func):
    if task_func not in authorizedTasks.list:
        print(f"task {task_func.__name__} is authorized")
        authorizedTasks.register_task(task_func)
    def wrapper(*args, **kwargs):
        return task_func(*args, **kwargs)
    return wrapper

secret_jwt = bytes(os.getenv('JWT_PRIVATE_PEM').encode('utf-8'))
public_jwt = bytes(os.getenv('JWT_PUBLIC_PEM').encode('utf-8'))

jwt_private_pem = serialization.load_pem_private_key(
    secret_jwt, password=None, backend=default_backend()
)

jwt_public_pem = serialization.load_pem_public_key(
    public_jwt, backend=default_backend()
)

use_jwt_expire = bool(os.getenv('USE_JWT_EXPIRE'))

jwt_algorithm = 'RS256'

if (use_jwt_expire):
    jwt_expire_time_sec = int(os.getenv('JWT_EXPIRE_SEC'))

def generate_new_jwt(payload: dict):
    if 'exp' not in payload and use_jwt_expire:
        max_timestamp = calendar.timegm(datetime.now(tz=timezone.utc).timetuple())+jwt_expire_time_sec
        payload['exp'] = str(max_timestamp)

    return jwt.encode(payload, jwt_private_pem, algorithm=jwt_algorithm), str(max_timestamp)

def abort_if_authorization_header_not_present():
    abort(401, message=f'This endpoint requires the "Authentication: Bearer JWT_token" header.')

def abort_if_jwt_is_expired():
    abort(401, message=f'This token signature has expired.')

def abort_if_jwt_is_invalid():
    abort(401, message=f'This token is invalid')

def abort_if_jwt_is_invalid_signature():
    abort(401, message=f'This token has invalid signature.')

def abort_if_jwt_unexpected_error():
    abort(401, message=f'An unexpected error occured during JWT decryption.')

def get_user_permissions(user:str, password:str):
    # You can implement here an algorithm to get a dictionary from database based on credentials.
    payload = {
        "allowed_tasks": {
            "myProtectedTask": True
        }
    }
    return payload

def verify_credentials(user:str, password:str):
    # You can implement here an algorithm to verify the credentials, e.g. verifying a bcrypt hash on database
    if user == "testuser" and password == "testpass":
        return True
    else:
        return False

def decrypt_jwt_authorization_header(auth_header):
    token = auth_header
    
    if 'Bearer' in token:

        token = token.split()[1]
        try:
            decoded = jwt.decode(token, jwt_public_pem, algorithms=[jwt_algorithm], verify_signature=True)
            return decoded

        except jwt.ExpiredSignatureError:
            abort_if_jwt_is_expired()
        except jwt.InvalidTokenError:
            abort_if_jwt_is_invalid()
        except jwt.InvalidSignatureError:
            abort_if_jwt_is_invalid_signature()
        except Exception as err:
            print(f"Unexpected error {err}, with type {type(err)}")
            abort_if_jwt_unexpected_error()
    else:
        abort_if_jwt_is_invalid()

def require_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
            
            if 'Bearer' in token:

                token = token.split()[1]
                try:
                    decoded = jwt.decode(token, jwt_public_pem, algorithms=[jwt_algorithm], verify_signature=True)
                    return func(decoded_payload=decoded, *args, **kwargs)

                except jwt.ExpiredSignatureError:
                    abort_if_jwt_is_expired()
                except jwt.InvalidTokenError:
                    abort_if_jwt_is_invalid()
                except jwt.InvalidSignatureError:
                    abort_if_jwt_is_invalid_signature()
                except Exception as err:
                    print(f"Unexpected error {err}, with type {type(err)}")
                    abort_if_jwt_inexpected_error()
            else:
                abort_if_jwt_is_invalid()
        else:
            abort_if_authorization_header_not_present()

    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    return wrapper