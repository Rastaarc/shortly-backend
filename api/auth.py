from .models import Links, Users
from flask import (
    request,
)
from functools import wraps
from flask_graphql_auth import (
    GraphQLAuth,
    get_jwt_data
)

from .utilities.constants import (
    USER_TYPES,
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
    try:
        claims = decode_token().get("user_claims")
        return claims
    except Exception as e:
        print(f"Get Claims Error: {e}")
        return None


def get_user_identity():
    try:
        identity = decode_token().get("identity")
        return identity
    except Exception as e:
        print(f"GetUserIdentity Error: {e}")
        return None


def is_valid_user(role):
    try:
        if get_claims() and get_user_identity() and get_claims().get("role") >= role:
            return True
        else:
            return False
    except Exception as e:
        print(f"Is_valid_user_error: {e}")
        return False


def valid_action_role(role=USER_TYPES.get("USER")):
    return is_valid_user(role)


def is_admin():
    return valid_action_role(USER_TYPES.get("ADMIN"))


def user_loggedin():
    return True if get_user_identity() else False


def user_from_identity():
    return Users.query.filter_by(username=get_user_identity()).first()


def request_by_owner(user_id):
    try:
        user = user_from_identity()

        return True if user.id == user_id else False
    except Exception as e:
        print(f"RequestByOwnerError: {e}")
        return False


def can_delete(id, what="link"):
    if not user_loggedin():
        return False

    try:

        if what == 'link':
            link = Links.query.filter_by(
                id=id, created_by_id=user_from_identity().id).first()
            return True if link else False
    except Exception as e:
        print(f"CanDeleteError: {e}")
        return False
