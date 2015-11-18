from django.db import models


class Article(models.Model):

    name = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
    author_id = models.IntegerField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ArticleCategories(models.Model):

    article = models.ForeignKey('Article')
    category = models.ForeignKey('Category')


class ArticleTags(models.Model):

    article = models.ForeignKey('Article')
    tag = models.ForeignKey('Tag')


