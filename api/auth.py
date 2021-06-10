from flask import (
    request,
)
from functools import wraps
from flask_graphql_auth import (
    GraphQLAuth,
    get_raw_jwt,
    decode_jwt,
    verify_jwt_in_argument,
    get_jwt_data
)

from .utilities.constants import (
    USER_TYPES,
    MESSAGES
)
from .graphql.objects import (
    ErrorObject,
)

auth = GraphQLAuth()

def decode_token():
    try:
        token = request.headers.get("Authorization").split("Bearer")[1]
        token = token.strip()

        data = get_jwt_data(token.encode('utf-8'), 'access')
        return data
    except Exception as e:
        print(f"Decode Token Error: {e}")
        return None

def get_claims():
    claims = decode_token().get("user_claims")
    return claims

def get_user_identity():
    identity = decode_token().get("identity")
    return identity

def is_valid_user(role):
    try:
        if get_claims() and get_user_identity() and get_claims().get("role") >= role:
            return True
        else:
            return False
    except Exception as e:
        print(f"Is_valid_user_error: {e}")
        return False




