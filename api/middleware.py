from .auth import (
    is_valid_user,
    valid_action_role,
    get_claims,
    get_user_identity,
    is_admin,
    request_by_owner,
    user_loggedin,
    can_modify,
)


class ContextMiddleware(object):
    def resolve(self, next, root, info, **args):
        context = info.context
        context.identity = get_user_identity
        try:
            context.role = get_claims().get('role')
        except Exception as e:
            context.user_role = -200
        context.valid_user = valid_action_role

        context.admin = is_admin
        context.loggedin = user_loggedin
        context.same_user = request_by_owner
        context.can_modify = can_modify

        return next(root, info, **args)
