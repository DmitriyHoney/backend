from rest_framework import generics
from .models import *
from .serializers import *


# Create your views here.
class ProblemListCreateView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemCommentListCreateView(generics.ListCreateAPIView):
    queryset = ProblemComment.objects.all()
    serializer_class = ProblemCommentSerializer


class ProblemPhotoCreateView(generics.ListCreateAPIView):
    queryset = ProblemPhoto.objects.all()
    serializer_class = ProblemPhotoSerializer


class ProblemCategoryList(generics.ListCreateAPIView):
    queryset = ProblemCategory.objects.all()
    serializer_class = ProblemCategorySerializer
    pagination_class = None


class ProblemCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProblemCategory.objects.all()
    serializer_class = ProblemCategorySerializer