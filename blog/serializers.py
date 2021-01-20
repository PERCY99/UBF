# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from . import models



class CategoriesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="categories")

    class Meta:
        model = models.categories
        fields = ("__all__")


class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="posts")
    comments = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = models.post
        fields = ("__all__")

    def get_comments(self, obj):
        comments = BlogPostCommentSerializer(obj.comments.all(),many=True).data
        return comments

    def get_likes(self, obj):
        likes = obj.likes.all().count()
        return likes

class BlogPostCommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="comment-detail")

    class Meta:
        model = models.comment
        fields = "__all__"