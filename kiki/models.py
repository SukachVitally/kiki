from django.db import models


class Article(models.Model):

    NEWS = 1
    BOOK = 2
    DOCUMENTATION = 3
    CATEGORIES = (
        (NEWS, 'News'),
        (BOOK, 'Books'),
        (DOCUMENTATION, 'Documentation')
    )

    name = models.CharField(max_length=50)
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
    author_id = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    category_id = models.IntegerField(choices=CATEGORIES, default=NEWS)

    def __str__(self):
        return self.name

    @property
    def category(self):
        for item in self.CATEGORIES:
            if item[0] == self.category_id:
                return item[1]
        return 'Without category'


class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ArticleTags(models.Model):

    article = models.ForeignKey('Article')
    tag = models.ForeignKey('Tag')


