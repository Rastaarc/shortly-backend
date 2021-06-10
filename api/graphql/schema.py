import graphene
from .queries import Query
from .mutations import Mutations


###################Schema###############################
schema = graphene.Schema(query=Query, mutation=Mutations)