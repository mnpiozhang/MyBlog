#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from models import Article
from django.core.urlresolvers import reverse

class ArticlesFeed(Feed):
    title = "Cloudhu lastest five news"
    link = "/rss/"
    description = "Cloudhu Blog new articles"

    def items(self):
        return Article.objects.order_by('-timestamp')[:5]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.timestamp

    def item_description(self, item):
        return item.content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('blogweb.views.showarticle', args=[item.id])