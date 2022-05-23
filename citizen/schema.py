import graphene
import graphql_jwt
from users.models import User
from users.schema import UpdateUser, UserType, CreateUser, ArchiveUser


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(root, info):
        return User.objects.all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    archive_user = ArchiveUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)