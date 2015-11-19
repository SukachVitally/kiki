"""kiki URL Configuration"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.get_articles),
    url(r'^login$', auth_views.login),
    url(r'^logout$', auth_views.logout, {'next_page': '/login'}),
    url(r'^registration$', views.registration),
    url(r'^articles/create$', views.create_article),
    url(r'^articles/(?P<article_id>[0-9]+)$', views.show_article),
    url(r'^articles/edit/(?P<article_id>[0-9]+)$', views.edit_article),
    url(r'^articles/delete/(?P<article_id>[0-9]+)$', views.delete_article),
    url(r'^articles/(?P<article_id>[0-9]+)/tags$', views.create_tag),
    url(r'^api/articles$', views.ArticlesApiView.as_view()),
    url(r'^api/articles/(?P<pk>[0-9]+)/$', views.ArticleApiView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
