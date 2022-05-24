import graphene
from django.contrib.auth.models import Group
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


class UserGroupsType(DjangoObjectType):
    class Meta:
        model = Group


class UserGenderEnum(graphene.Enum):
    MALE = User.MALE
    FEMALE = User.FEMALE


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


class CreateUserGroup(graphene.Mutation):
    message = ObjectField()
    group = graphene.Field(UserGroupsType)

    class Arguments:
        name = graphene.String()

# only is_authenticated, admin || moder
class UpdateUser(graphene.Mutation):
    message = ObjectField()
    user = graphene.Field(UserType)

    class Arguments:
        id = graphene.ID(required=True)
        is_active = graphene.Boolean()
        firstname = graphene.String()
        lastname = graphene.String()
        middlename = graphene.String()
        gender = UserGenderEnum()
        groups = graphene.List(graphene.ID)

    @classmethod
    def mutate(cls, root, info, id=None, **kwargs):
        user = User.objects.get(id=id) if id else info.context.user
        avatar = info.context.FILES.get('avatar', None)
        serializer = UserSerializer(user, data=kwargs, partial=True)
        user = None
        msg = None
        if serializer.is_valid():
            user = serializer.save()
            if avatar:
                user.create_avatar_thumb(avatar)
        else:
            msg = serializer.errors
        return cls(user=user, message=msg)


class UpdateCurrentUser(UpdateUser):
    class Arguments:
        is_active = graphene.Boolean()
        is_superuser = graphene.Boolean()


#TODO create UpdateCurrentUser by JWT
 

# only is_authenticated and roles admin or moder
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


#TODO create ForgetPassword with email callback


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
