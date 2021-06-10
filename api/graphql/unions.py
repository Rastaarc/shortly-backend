from graphene import (
    Union,
)
from .objects import (
    ClicksObject,
    ErrorObject,
    UsersObject,
    LinksObject,
    SubscriptionsObject,
    UsersSubscriptionsObject
)


class ProctectedUsers(Union):
    class Meta:
        types = (UsersObject, ErrorObject)


class ProtectedLinks(Union):
    class Meta:
        types = (LinksObject, ErrorObject)