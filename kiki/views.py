import bleach
from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponseForbidden

from kiki import forms
from kiki import models
from kiki.serializers import ArticleSerializer


@login_required
def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                return redirect('/login')
            form.add_error('username', 'User already exist')
    else:
        form = forms.RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


@login_required
def create_article(request):
    if request.method == 'POST':
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            article = models.Article.objects.create(
                name=form.cleaned_data['name'],
                text=bleach.clean(form.cleaned_data['text']),
                category_id=form.cleaned_data['category'],
                author_id=request.user.id
            )
            article.save()
            return redirect('/')
    else:
        form = forms.ArticleForm()
    return render(request, 'article/create.html',  {'form': form})


@login_required
def get_articles(request):
    articles = models.Article.objects.all().filter(author_id=request.user.id)
    return render(request, 'article/list.html',  {'articles': articles})


@login_required
def show_article(request, article_id):
    try:
        article = models.Article.objects.get(pk=article_id)
    except models.Article.DoesNotExist:
        return Http404('Article not exist')

    return render(request, 'article/show.html', {
        'article': article,
        'similar_articles': article.similar_articles()
    })


@login_required
def edit_article(request, article_id):
    try:
        article = models.Article.objects.get(pk=article_id)
    except models.Article.DoesNotExist:
        return Http404('Article not exist')

    if article.author_id != request.user.id:
        return HttpResponseForbidden('its not yours article')

    if request.method == 'POST':
        form = forms.ArticleForm(request.POST)
        if form.is_valid():
            article.name = form.cleaned_data['name']
            article.text = bleach.clean(form.cleaned_data['text'])
            article.category_id = form.cleaned_data['category']
            article.save()
            return redirect('/')
    else:
        form = forms.ArticleForm(initial={'name': article.name, 'text': article.text, 'category': article.category_id})
    return render(request, 'article/update.html',  {'form': form, 'article_id': article.id})


@login_required
def delete_article(request, article_id):
    try:
        article = models.Article.objects.get(pk=article_id)
    except models.Article.DoesNotExist:
        return Http404('Article not exist')

    if article.author_id != request.user.id:
        return HttpResponseForbidden('its not yours article')

    article.delete()
    return redirect('/')


@login_required
def create_tag(request, article_id):
    try:
        article = models.Article.objects.get(pk=article_id)
    except models.Article.DoesNotExist:
        return Http404('Article not exist')

    if article.author_id != request.user.id:
        return HttpResponseForbidden('its not yours article')

    if request.method == 'POST':
        form = forms.TagFrom(request.POST)
        if form.is_valid():
            try:
                tag = models.Tag.objects.get(name=form.cleaned_data['name'])
            except models.Tag.DoesNotExist:
                tag = models.Tag(name=form.cleaned_data['name'])
                tag.save()

            if not models.ArticleTags.objects.filter(article_id=article.id, tag_id=tag.id).count():
                article_tag = models.ArticleTags(article_id=article.id, tag_id=tag.id)
                article_tag.save()

    form = forms.TagFrom()
    tags = models.ArticleTags.objects.all().filter(article_id=article.id)
    return render(request, 'article/tag.html',  {'form': form, 'tags': tags})


class ArticlesApiView(generics.ListAPIView):
    queryset = models.Article.objects.all().filter(is_approved=True)
    serializer_class = ArticleSerializer


class ArticleApiView(generics.RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = ArticleSerializer