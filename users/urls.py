from django.urls import path, include
from .views import UserList, UserDetail, UserGroups, UserChangePasswordView, \
    UserChangeEmailView, CustomTokenObtainPairView, UserCurrent
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('', UserList.as_view()),
    # path('<int:pk>/', UserDetail.as_view()),
    # path('groups', UserGroups.as_view()),
    # path('change_password/', UserChangePasswordView.as_view()), # только авторизованным
    # path('change_email/', UserChangeEmailView.as_view()), # только авторизованным
    # path('current/', UserCurrent.as_view()),
    #
    # path('signin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh')
]
