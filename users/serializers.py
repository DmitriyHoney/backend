from dataclasses import fields
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from django.contrib.auth.models import Group


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["user"] = UserSerializer(self.user).data
        data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        del data["refresh"]
        del data["access"]
        return data


class GroupSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, group):
        groups = {
            'admin': 'Администратор',
            'user': 'Пользователь',
            'moderator': 'Модератор'
        }

        return groups.get(str(group.name), None)

    class Meta:
        model = Group

        fields = ('id', 'name', 'title', )


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    short_name = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    def get_groups(self, instance):
        groups = instance.groups.all().order_by('pk')
        return GroupSerializer(instance=groups, many=True, read_only=True).data

    class Meta:
        model = User
        exclude = ['user_permissions', 'last_login', 'password']

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_short_name(self, obj):
        return obj.get_short_name()


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label="Пароль")

    def get_fields(self, *args, **kwargs):
        fields = super(UserDetailSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        fields['avatar_small'].read_only = True
        if request and request.method in ['PUT', 'PATCH']:
            fields['password'].read_only = True
            fields['email'].read_only = True
            if not request.user.is_superuser:
                fields['groups'].read_only = True

        return fields

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        groups = None
        if validated_data.get('groups'):
            groups = validated_data.pop('groups')
        password = validated_data.get('password', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.create_avatar_thumb()

        if groups:
            user.groups.set(groups)

        return user

    def update(self, instance, validated_data):
        groups = validated_data.get('groups', None)
        if groups:
            groups = validated_data.pop('groups')
            instance.groups.set(groups)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.create_avatar_thumb()
        return instance

    def to_representation(self, instance):
        return UserSerializer(instance).data


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeEmailSerializer(serializers.Serializer):
    model = User
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True)


