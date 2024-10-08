from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "user"]
