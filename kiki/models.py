from django.db import models
from django.db.models import Count


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

    def tags(self):
        article_tags = ArticleTags.objects.all().filter(article_id=self.id)
        return [item.tag for item in article_tags]

    def similar_articles(self):
        tag_ids = [tag.id for tag in self.tags()]
        tag_list = ArticleTags.objects.filter(tag_id__in=tag_ids)\
            .values('article_id')\
            .annotate(dcount=Count('article_id'))\
            .order_by('dcount')\
            .reverse()

        article_ids = [i['article_id'] for i in tag_list]
        if not len(article_ids):
            return []

        # remove own id from list
        article_ids.remove(self.id)
        articles = list(Article.objects.filter(pk__in=article_ids))
        articles.sort(key=lambda t: article_ids.index(t.pk))
        return articles


class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ArticleTags(models.Model):

    article = models.ForeignKey('Article')
    tag = models.ForeignKey('Tag')


