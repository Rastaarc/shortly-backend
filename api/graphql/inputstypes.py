from graphene import (
    InputObjectType,
    String,
    Int,
)

class AccountInputs(InputObjectType):
    username = String(required=True)
    email = String(required=True)
    password = String(required=True)



class LinkInputs(InputObjectType):
    link = String(required=True)
    keyword = String(required=True)