import graphene
import graphql_jwt
from users.models import User
from users.schema import UpdateUser, UserType, CreateUser, ArchiveUser, ObtainJSONWebToken
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())
    users = graphene.List(UserType)

    @login_required
    def resolve_user(root, info, id=None):
        if id:
            return User.objects.get(id=id)

    def resolve_users(root, info):
        # user = info.context.user
        return User.objects.all()


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    archive_user = ArchiveUser.Field()
    signin = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)