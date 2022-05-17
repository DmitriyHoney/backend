import graphene
from users.models import User
from users.schema import UserType, CreateUser, CreateUserDRF

# graphene.types.scala


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    # problems = graphene.Field(
    #     ProblemType,
    #     id=graphene.Int(required=True)
    # )

    def resolve_users(root, info):
        return User.objects.all()

    # def resolve_problems(root, info, id):
    #     try:
    #         return Problem.objects.get(id=id)
    #     except Problem.DoesNotExist:
    #         return None


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_user_drf = CreateUserDRF.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)