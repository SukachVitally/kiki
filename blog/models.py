from django.db import models


class Article(models.Model):

    db_table = 'articles'

    name = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.name


class ArticleCategories(models.Model):

    db_table = 'article_categories'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ArticleTags(models.Model):

    db_table = 'article_tags'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
