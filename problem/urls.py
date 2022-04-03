from django.urls import path
from .views import *


urlpatterns = [
    path('', ProblemListCreateView.as_view()),
    path('commentadd/', ProblemCommentListCreateView.as_view()),
    path('attach-photo/', ProblemPhotoCreateView.as_view()),
    path('category/', ProblemCategoryList.as_view()),
    path('category/<int:pk>/', ProblemCategoryDetail.as_view()),
]
