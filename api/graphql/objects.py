from graphene import (
    relay,
    String,
    Int,
    ID,
    ObjectType,
    List,
    Field,
)
import graphene

from graphene_sqlalchemy import (
    SQLAlchemyObjectType
)
from sqlalchemy.engine import interfaces
from ..models import (
    Clicks,
    Users,
    Links,
    UsersSubscriptions,
    Subscriptions,

)
from ..utilities.constants import (
    ERROR_CODES,
    ITEMS_PER_PAGE,
)


class ErrorObject(ObjectType):
    message = String()
    code = Int(default_value=ERROR_CODES.get("UNAUTHORIZED", 401))


# Users
class UsersObject(SQLAlchemyObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = Users
        exclude_fields = ("password_hash",)
        interfaces = (relay.Node,)

    def resolve_id(root, info):
        return root.id


class LinksObject(SQLAlchemyObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = Links
        interfaces = (relay.Node,)

    def resolve_id(root, info):
        return root.id


class ClicksObject(SQLAlchemyObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = Clicks
        interfaces = (relay.Node,)

    def resolve_id(root, info):
        return root.id


class SubscriptionsObject(SQLAlchemyObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = Subscriptions
        interfaces = (relay.Node,)

    def resolve_id(root, info):
        return root.id


class UsersSubscriptionsObject(SQLAlchemyObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = UsersSubscriptions
        interfaces = (relay.Node,)

    def resolve_id(root, info):
        return root.id


###########PAGINATED OBJECTS##############
class PaginationObject(ObjectType):
    page = graphene.Int(required=True)
    per_page = graphene.Int(required=True)
    total = graphene.Int(required=True)


class PaginatedLinksObject(PaginationObject):
    links = graphene.List(lambda: LinksObject)


class PaginatedUsersObject(PaginationObject):
    users = graphene.List(lambda: UsersObject)


#########################################
class UsersObject1(ObjectType):
    id = ID(required=True)
    username = String(required=True)
    user_type = String(required=True)
    email = String(required=True)
    join_date = String(required=True)
    links = List(lambda: LinksObject1)

    """
    def resolve_password(root,info):
        print(root.metadata)
        return root.password_hash

    def resolve_links(root, info):
        print(root)
        links_ = Links.query.filter_by(created_by_id=root.id)
        print(links_)
        return links_
    """


class LinksObject1(ObjectType):
    id = ID(required=True)
    original_link = String(required=True)
    short_link = String(required=True)
    created_at = String(required=True)
    created_by = Field(lambda: UsersObject1)


class OverviewObjects(ObjectType):
    total_links = Int(required=True)
    total_clicks = Int(required=True)
    total_users = Int(required=True)
