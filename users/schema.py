import graphene
from django.db import transaction
from graphene import Scalar
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
import graphql_jwt
from graphql_jwt.decorators import login_required, superuser_required, user_passes_test, permission_required

from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer


class ObjectField(Scalar): # to serialize error message from serializer
    @staticmethod
    def serialize(dt):
        return dt 


class UserType(DjangoObjectType):
    class Meta:
        model = User
        convert_choices_to_enum = False
        exclude = ['password']


class CreateUser(graphene.Mutation):
    message = ObjectField()
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String()
        password = graphene.String()
        phone = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        serializer = UserSerializer(data=kwargs)
        user = None
        msg = None
        if serializer.is_valid():
            user = serializer.save()
        else:
            msg = serializer.errors
        return cls(user=user,message=msg)


class UpdateUser(graphene.Mutation):
    message = ObjectField()
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        is_active = graphene.Boolean()
        is_superuser = graphene.Boolean()
        # groups = graphene.List(graphene.ID())

    @classmethod
    def mutate(cls, root, info, id, **kwargs):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=kwargs, partial=True)
        user = None
        msg = None
        if serializer.is_valid():
            user = serializer.save()
        else:
            msg=serializer.errors
        return cls(user=user,message=msg)


class ArchiveUser(graphene.Mutation):
    message = ObjectField()
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return cls(user=user, message='success')


# only is_authenticated
class ChangePassword(graphene.Mutation):
    message = ObjectField()
    user = graphene.Field(UserType)

    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        serializer = ChangePasswordSerializer(data=kwargs)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return cls(user=None, message='error') 
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return cls(user=user, message='success')
        else:
            return cls(user=None, message=serializer.errors)


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
