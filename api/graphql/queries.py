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
    OverviewObjects,
    PaginatedLinksObject,
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
    get_user_identity,
    get_claims,
)
from ..utilities.constants import (
    ITEMS_PER_PAGE,
    USER_TYPES,
    MESSAGES,
    ERROR_CODES,
)
from .unions import (
    ProctectedUsers,
    ProtectedLinks,
    ProtectedOverview,
)
# from sqlalchemy import (
#     desc,
#     func,
# )

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

    ########################LINKS########################################
    total_links = Int(required=True, user_id=Int())

    def resolve_total_links(root, info, user_id=None):
        total = -1

        if info.context.admin():
            if user_id:
                total = Links.query.filter_by(created_by_id=user_id).count()
            else:
                total = Links.query.count()
        elif info.context.same_user(user_id):
            total = Links.query.filter_by(created_by_id=user_id).count()

        return total

    get_all_links = List(ProtectedLinks,
                         page=ID(),
                         per_page=ID(),
                         search=String(),)

    def resolve_get_all_links(root, info, page=None, per_page=None, search=None):
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

    get_user_links = Field(ProtectedLinks,
                           user_id=Int(required=True),
                           page=Int(),
                           per_page=Int(),
                           search=String(),
                           )

    def resolve_get_user_links(root, info, user_id, page=None, per_page=None, search=None):
        if is_valid_user(USER_TYPES.get("USER")):
            identity = get_user_identity()
            user = Users.query.filter_by(id=int(user_id)).first()
            if not user:
                return ErrorObject(message=MESSAGES.get("NO_USER"), code=ERROR_CODES.get("NOT_FOUND"))
            else:
                role = get_claims().get('role')
                admin = USER_TYPES.get("ADMIN")
                if role < admin and user.username != identity:
                    return ErrorObject(message=MESSAGES.get("NO_ACCESS"))

            try:
                if not page:
                    page = 1

                if not per_page:
                    per_page = ITEMS_PER_PAGE

                query = LinksObject.get_query(info)

                result = None
                if not search:
                    result = query.filter_by(
                        created_by_id=int(user_id)
                    ).order_by(Links.created_at.desc()).paginate(page=int(page), per_page=int(per_page))
                    # print(**result)
                else:
                    print(search)
                    result = query.filter_by(created_by_id=int(user_id))
                    result = result.filter(Links.short_link.ilike(
                        f"%{search}%") | Links.original_link.ilike(f"%{search}%"))
                    result = result.order_by(Links.created_at.desc()).paginate(
                        page=int(page), per_page=int(per_page))

                return PaginatedLinksObject(page=result.page,
                                            per_page=per_page,
                                            total=result.total,
                                            links=result.items
                                            )
            except Exception as e:
                print(f"Get User Links Error: {e}")
                return ErrorObject(message=MESSAGES.get("UNKNOWN_ERROR"), code=ERROR_CODES.get("INTERNAL_ERROR"))
        else:
            return ErrorObject(message=MESSAGES.get("NO_ACCESS"))

    #########################Clicks################################
    total_clicks = Int(required=True, user_id=Int())

    def resolve_total_clicks(root, info, user_id=None):
        total = -1

        if info.context.admin():
            if user_id:
                total = Links.query.filter_by(
                    created_by_id=user_id).first().clicks.count()
            else:
                total = Clicks.query.count()
        elif info.context.same_user(user_id):
            total = Links.query.filter_by(
                created_by_id=user_id).first().clicks.count()

        return total

    #################################DASHBOARD OVERVIEW################
    # get_overview_counts = Field(ProtectedOverview, id=Int())

    # def resolve_get_overview_counts(root, info, id=None):
    #     if not is_valid_user(USER_TYPES.get("USER")):
    #         return ErrorObject(message=MESSAGES.get("NO_ACCESS"))

    #     identity = get_user_identity()
    #     print(identity)

    #     role = get_claims().get('role')
    #     admin = USER_TYPES.get("ADMIN")
    #     if not id and role == admin:
    #         counters = {
    #             'total_links': Links.query.count(),
    #             'total_users': Users.query.count(),
    #             'total_clicks': Clicks.query.count(),
    #         }
    #         return OverviewObjects(**counters)

    #     elif id and role < admin:
    #         user = Users.query.filter_by(username=identity).first()
    #         counters = {
    #             'total_links': Links.query.filtery_by(created_by_id=user.id).count(),
    #             'total_users': 0,
    #             'total_clicks': Links.query.filtery_by(created_by_id=user.id).clicks.count(),
    #         }
    #         return OverviewObjects(**counters)
    #     else:
    #         return ErrorObject(message=MESSAGES.get("NO_ACCESS"))
