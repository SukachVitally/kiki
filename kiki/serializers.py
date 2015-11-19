from rest_framework import serializers
import models


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ('id', 'name')


class ArticleSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True)

    class Meta:
        model = models.Article
        fields = ('id', 'name', 'text', 'tags')
