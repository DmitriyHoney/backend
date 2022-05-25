import graphene
import graphql_jwt
from users.models import User
from django.contrib.auth.models import Group
from users.schema import UserType, UserGroupsType, CreateUser, ObtainJSONWebToken, UpdateUser, UpdateCurrentUser, ArchiveUser, ChangePassword, CreateUserGroup
from graphql_jwt.decorators import login_required
#TODO Permissions access 


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())
    users = graphene.List(
        UserType,
        limit=graphene.Int(),
        offset=graphene.Int()
    )
    groups = graphene.List(UserGroupsType)

    def resolve_user(root, info, id=None):
        if id:
            return User.objects.get(id=id)

    def resolve_users(root, info, limit=None, offset=None):
        qs = User.objects.all()

        if offset:
            qs = qs[offset:]

        if limit:
            qs = qs[:limit]

        return qs



    def resolve_groups(root, info):
        return Group.objects.all()


class Mutation(graphene.ObjectType):
    createGroup = CreateUserGroup.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    update_current_user = UpdateCurrentUser.Field()
    archive_user = ArchiveUser.Field()
    signin = ObtainJSONWebToken.Field()
    change_password = ChangePassword.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)