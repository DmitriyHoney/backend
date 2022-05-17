import graphene
from graphene import Scalar
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
from .models import User
from .serializers import UserDetailSerializer


class UserType(DjangoObjectType):
    class Meta:
        model = User
        convert_choices_to_enum = False
        exclude = ['password']


class CreateUser(graphene.Mutation):
    """
    This is the main class where user object is created.
    This class must implement a mutate method.
    """
    class Arguments:
        email = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()
        password = graphene.String()
        phone = graphene.String()

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, root, info, **user_data):
        user = User(
            firstname=user_data.get('firstname'),
            email=user_data.get('email'),
            lastname=user_data.get('lastname'),
            phone=user_data.get('phone')
        )
        user.set_password(user_data.get('password'))  # This will hash the password
        user.save()
        return CreateUser(user=user)


class ObjectField(Scalar): # to serialize error message from serializer
    @staticmethod
    def serialize(dt):
        return dt


class CreateUserDRF(SerializerMutation):
    class Meta:
        serializer_class = UserDetailSerializer
        model_class = User