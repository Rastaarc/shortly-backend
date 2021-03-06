import re
from flask import (
    current_app,
)
import graphene
from .inputstypes import (
    AccountInputs,
    LinkInputs,
)
from ..models import (
    Links,
    db,
    Users,
)
from .objects import (
    LinksObject,
    UsersObject,
    ClicksObject,
    UsersSubscriptionsObject,
    SubscriptionsObject,
    UsersObject1,
)
from ..utilities.constants import (
    MESSAGES,
    URL_PREFIX,
    USER_TYPES,
)
from ..utilities.link import (
    create_short_link,
    create_short_link_free,
    valid_link,
)
from flask_graphql_auth import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from ..auth import (
    is_valid_user,
    get_user_identity,
    get_claims,
    decode_token,
)


class CreateAccount(graphene.Mutation):
    class Arguments:
        account_data = AccountInputs(required=True)

    user = graphene.Field(UsersObject)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, account_data=None):
        try:
            user_by_username = Users.query.filter_by(
                username=account_data.username).first()
            if user_by_username:
                return CreateAccount(ok=False, message=MESSAGES.get("USER_EXIST"))

            user_by_email = Users.query.filter_by(
                email=account_data.email).first()
            if user_by_email:
                return CreateAccount(ok=False, message=MESSAGES.get("EMAIL_EXIST"))

            # validate username
            username_reg = r"^[a-zA-Z0-9_]{5,30}$"
            if not re.match(username_reg, account_data.username):
                return CreateAccount(ok=False, message=MESSAGES.get("INVALID_USERNAME"))
            # validate email
            email_reg = r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
            if not re.match(email_reg, account_data.email):
                return CreateAccount(ok=False, message=MESSAGES.get("INVALID_EMAIL"))

            # validate password
            password_reg = r"^[a-zA-Z_@]{5,30}$"
            if not re.match(password_reg, account_data.password):
                return CreateAccount(ok=False, message=MESSAGES.get("INVALID_PASSWORD"))

            user = Users(
                username=account_data.username,
                email=account_data.email
            )

            admin_u = current_app.config.get("ADMIN_U")
            admin_p = current_app.config.get("ADMIN_P")
            if account_data.username == admin_u and account_data.password == admin_p:
                user.user_type = USER_TYPES.get("ADMIN")

            user.password = account_data.password
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            message = MESSAGES.get("UNKNOWN_ERROR")
            ok = False
        else:
            message = MESSAGES.get("NEW_ACCOUNT_SUCCESS")
            ok = True
        return CreateAccount(user=user, ok=ok, message=message)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    status = graphene.Boolean(required=True)
    message = graphene.String(required=True)

    def mutate(root, info, id):
        message = MESSAGES.get('DELETE_SUCC')
        status = False
        if info.context.admin():
            try:
                user = Users.query.filter_by(id=id).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    status = True
            except Exception as e:
                print(f"DeleteUserError: {e}")
                message = MESSAGES.get('DELETE_ERR')
        else:
            status = False
            message = MESSAGES.get('NO_ACCESS')

        return DeleteUser(status=status, message=message)


class LoginUser(graphene.Mutation):
    class Arguments:
        username_or_email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UsersObject)
    logged_in = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, username_or_email, password):
        # print(info.context.headers)  # .get("Authorization")
        user = Users.query.filter_by(username=username_or_email).first()
        if not user:
            user = Users.query.filter_by(email=username_or_email).first()

        if user and user.valid_passkey(password):
            message = MESSAGES.get("LOGIN_SUC")
            logged_in = True
            return LoginUser(
                user=user,
                logged_in=logged_in,
                message=message,
                token=create_access_token(user.username, user_claims={
                                          "role": user.user_type})
            )
        else:
            message = MESSAGES.get("LOGIN_ERR")
            logged_in = False
            return LoginUser(
                # user=None,
                logged_in=logged_in,
                message=message,
                token=None
            )


class CreateLinkByUser(graphene.Mutation):
    class Arguments:
        user_input = LinkInputs(required=True)

    link = graphene.Field(LinksObject)
    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(root, info, user_input):
        link = None
        valid = False
        message = MESSAGES.get("NO_ACCESS")
        ok = False
        try:
            valid = is_valid_user(USER_TYPES.get("USER"))
        except Exception as e:
            print(f'Valid User Error: {e}')

        if valid:
            if not valid_link(user_input.link):
                message = MESSAGES.get("INVALID_LINK_")
                ok = False
            elif len(user_input.keyword) < 3 or len(user_input.keyword) > 30:
                message = MESSAGES.get("INVALID_LINK_KEYWORD")
                ok = False
            else:
                try:
                    identity = get_user_identity()
                    short_link = create_short_link(user_input.keyword)
                    user = Users.query.filter_by(username=identity).first()
                    link = Links(
                        created_by=user,
                        short_link=short_link,
                        original_link=user_input.link
                    )
                    db.session.add(link)
                    db.session.commit()
                    message = MESSAGES.get("_LINK_CREATED_SUC")
                    ok = True
                except Exception as e:
                    print(f"Error Creating Link: {e}")
                    message = MESSAGES.get("_LINK_CREATED_ERR")
                    ok = False

        return CreateLinkByUser(link=link, ok=ok, message=message)


class CreateShortLinkFree(graphene.Mutation):
    class Arguments:
        original_link = graphene.String(required=True)

    link = graphene.Field(LinksObject)
    message = graphene.String()
    ok = graphene.Boolean()

    def mutate(root, info, original_link):
        ok = False
        link = None

        if not valid_link(original_link):
            message = MESSAGES.get("INVALID_LINK_")
        else:
            try:
                short = create_short_link_free()
                link = Links(original_link=original_link,
                             short_link=short,
                             created_by=Users.query.filter_by(
                                 username="FreeUsers").first()
                             )

                if decode_token():
                    user = Users.query.filter_by(
                        username=get_user_identity()).first()
                    link.created_by = user

                db.session.add(link)
                db.session.commit()
                message = MESSAGES.get("_LINK_CREATED_SUC")
                ok = True
            except Exception as e:
                print(f"Error Creating Link(Free): {e}")
                message = MESSAGES.get("_LINK_CREATED_ERR")

        return CreateShortLinkFree(link=link, ok=ok, message=message)


class DeleteLink(graphene.Mutation):
    class Arguments:
        link_id = graphene.Int(required=True)

    status = graphene.Boolean(required=True)
    message = graphene.String(required=True)

    def mutate(root, info, link_id):
        status = False
        message = MESSAGES.get("DELETE_ERR")
        if info.context.admin() or info.context.can_modify(link_id):
            try:
                link = Links.query.filter_by(id=link_id).first()
                if link:
                    db.session.delete(link)
                    db.session.commit()
                    status = True
                    message = MESSAGES.get("DELETE_SUCC")
                else:
                    message = MESSAGES.get("NO_RECORD_TO_DELETE")
            except Exception as e:
                print(f"DeleteLinkError: {e}")

        else:
            message = MESSAGES.get("NO_ACCESS")

        return DeleteLink(status=status, message=message)


class UpdateLink(graphene.Mutation):
    class Arguments:
        link_id = graphene.Int(required=True)
        o_link = graphene.String(required=True)
        keyword = graphene.String(required=True)

    message = graphene.String()
    ok = graphene.Boolean()
    link = graphene.Field(LinksObject)

    def mutate(root, info, link_id, o_link, keyword):
        ok = False
        message = MESSAGES.get("UPDATE_ERR")
        link = None

        if info.context.admin() or info.context.can_modify(link_id):
            try:
                link_data = Links.query.filter_by(id=link_id).first()

                if link_data:
                    link_data.original_link = o_link
                    link_data.short_link = create_short_link(keyword)

                    db.session.add(link_data)
                    db.session.commit()

                    ok = True
                    message = MESSAGES.get("UPDATE_SUCC")
                else:
                    message = MESSAGES.get("NO_RECORD_TO_UPDATE")

            except Exception as e:
                print(f"UpdateLinkError: {e}")
        else:
            message = MESSAGES.get("NO_ACCESS")

        return UpdateLink(link=link, ok=ok, message=message)


#####################MUTATIONS############################
##########################################################


class Mutations(graphene.ObjectType):
    create_account = CreateAccount.Field()
    delete_user = DeleteUser.Field()

    login_account = LoginUser.Field()

    create_premium_link = CreateLinkByUser.Field()
    create_freemium_link = CreateShortLinkFree.Field()
    delete_link = DeleteLink.Field()
    update_link = UpdateLink.Field()
