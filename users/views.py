from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import User
from django.contrib.auth.models import Group
from .serializers import UserSerializer, UserDetailSerializer, GroupSerializer, ChangePasswordSerializer, ChangeEmailSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = ()

class UserGroups(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class UserList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        queryset = User.objects.all()
        is_archive = self.request.query_params.get('is_archive', False)
        return queryset.filter(is_archive=True) if is_archive else queryset.filter(is_archive=False)

    def get_serializer_class(self):
        method = self.request.method
        if method in ['POST']:
            return UserDetailSerializer
        return UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        # TODO: сделать собственный класс с обработчиками ответов
        not_found_response = Response({"msg": "object not found"}, status=status.HTTP_404_NOT_FOUND)
        success_delete_response = Response(status=status.HTTP_204_NO_CONTENT)
        if not pk:
            return not_found_response
        try:
            user = User.objects.get(pk=pk)
            user.is_archive = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return success_delete_response

class UserChangePasswordView(generics.CreateAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Неверный пароль."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(data={"message": "Пароль успешно изменён"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserChangeEmailView(generics.UpdateAPIView):
    model = User
    serializer_class = ChangeEmailSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('password')):
                return Response({"password": ["Неверный пароль."]}, status=status.HTTP_400_BAD_REQUEST)
            user.email = serializer.data.get('email')
            user.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCurrent(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        self.queryset = User.objects.get(pk=self.request.user.pk)
        return Response(UserDetailSerializer(self.queryset).data, status=status.HTTP_200_OK)