"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from views import index,showarticle,searchtag,aboutme,archive,tags,itPopularBooks,novelPopularBooks,toys,searchtitle,flashtime,randomtool,dogfood
from feeds import ArticlesFeed
from api import jdBooksApi

urlpatterns = [         
    url(r'^index/(\d*)', index),
    url(r'^show/(\d+)/$',showarticle),
    url(r'^tag/(?P<tagname>\w+)/(?P<page>\d*)$',searchtag),
    url(r'^about/$',aboutme),
    url(r'^archive/$',archive),
    url(r'^tag/$',tags),
    url(r'^rss/$',ArticlesFeed()),
    url(r'^toys/$',toys),
    url(r'^toys/itpopularbooks/$',itPopularBooks),
    url(r'^toys/novelpopularbooks/$',novelPopularBooks),
    url(r'^toys/flashtime/$',flashtime),
    url(r'^search',searchtitle),
    url(r'^randomtool/',randomtool),
    url(r'^dogfood/',dogfood),
    url(r'^jdbooks/',jdBooksApi.as_view())
]
