from graphene import (
    Union,
)
from .objects import (
    ClicksObject,
    ErrorObject,
    UsersObject,
    LinksObject,
    SubscriptionsObject,
    UsersSubscriptionsObject,
    PaginatedLinksObject,
    PaginatedUsersObject,
    OverviewObjects,
)


class ProctectedUsers(Union):
    class Meta:
        types = (UsersObject, ErrorObject)


class ProtectedLinks(Union):
    class Meta:
        types = (PaginatedLinksObject, ErrorObject)


class ProtectedOverview(Union):
    class Meta:
        types = (OverviewObjects, ErrorObject)
