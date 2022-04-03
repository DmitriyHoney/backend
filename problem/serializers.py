from rest_framework import serializers
from .models import Problem, ProblemComment, ProblemPhoto, ProblemCategory


class ProblemSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return ProblemCommentSerializer(obj.problemcomment_set, many=True).data

    class Meta:
        model = Problem
        fields = '__all__'


class ProblemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemComment
        fields = '__all__'


class ProblemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemPhoto
        fields = '__all__'


class ProblemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCategory
        fields = '__all__'