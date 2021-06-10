from flask import (
    request,
)
from graphene import (
    String,
    Int,
    relay,
    ObjectType,
    Float,
    List,
    Field,
    ID,
)
from .mutations import (
    CreateAccount,
)
from graphene_sqlalchemy import (
    SQLAlchemyConnectionField,
)
from .objects import (
    ErrorObject,
    LinksObject1,
    UsersObject,
    UsersObject1,
    LinksObject,
    ClicksObject,
    SubscriptionsObject,
    UsersSubscriptionsObject,
)

from ..models import(
    db,
    Users,
    Links,
    Subscriptions,
    UsersSubscriptions,
    Clicks,
)
from ..auth import (
    is_valid_user,
)
from ..utilities.constants import (
    USER_TYPES,
    MESSAGES,
)
from .unions import (
    ProctectedUsers,
    ProtectedLinks,
)


#####################QUERIES############################
##########################################################
class Query(ObjectType):
    node = relay.Node.Field()
    #all_users = SQLAlchemyConnectionField(UsersObject)
    #all_links = SQLAlchemyConnectionField(LinksObject)
    #all_clicks = SQLAlchemyConnectionField(ClicksObject)
    #all_subscriptions = SQLAlchemyConnectionField(SubscriptionsObject)
    #all_users_subscriptions = SQLAlchemyConnectionField(UsersSubscriptionsObject)

    get_users = List(UsersObject1)
    def resolve_get_users(root, info):
        return Users.query.all()

    ########################USERS########################################

    get_all_users = List(ProctectedUsers)
    def resolve_get_all_users(root, info):
        data = []
        if is_valid_user(USER_TYPES.get("USER")):
            data = UsersObject.get_query(info).all()
        else:
            data = [ErrorObject(message=MESSAGES.get("NO_ACCESS"))]
        return data



    get_user = Field(ProctectedUsers, username_or_email=String(required=True))
    def resolve_get_user(root, info, username_or_email):
        if is_valid_user(USER_TYPES.get("USER")):
            user_query = UsersObject.get_query(info)

            user = user_query.filter_by(username=username_or_email).first()
            if not user:
                user = user_query.filter_by(email=username_or_email).first()
            if user:
                return user
        else:
            return ErrorObject(message=MESSAGES.get("NO_ACCESS"))



    get_user_by_id = Field(ProctectedUsers, id=ID(required=True))
    def resolve_get_user_by_id(root, info, id):
        if is_valid_user(USER_TYPES.get("USER")):
            query = UsersObject.get_query(info)
            user = query.filter_by(id=id).first()
            return user
        else:
            return ErrorObject(message=MESSAGES.get("NO_ACCESS"))

        """TODO: UPDATE USER"""



    ########################LIST########################################
    get_all_links = List(ProtectedLinks)
    def resolve_get_all_links(root, info):
        if is_valid_user(USER_TYPES.get("USER")):
            return LinksObject.get_query(info).all()
        else:
            return [ErrorObject(message=MESSAGES.get("NO_ACCESS"))]

    get_link_by_id = Field(ProtectedLinks, id=ID(required=True))
    def resolve_get_link_by_id(root, info, id):
        if is_valid_user(USER_TYPES.get("USER")):
            query = LinksObject.get_query(info)
            link = query.filter_by(id=id).first()
            return link
        else:
            return ErrorObject(message=MESSAGES.get("NO_ACCESS"))

        """TODO: UPDATE LINK"""