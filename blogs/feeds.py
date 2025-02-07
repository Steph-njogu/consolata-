from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import NewsArticle

class LatestFeed(Feed):
    title = "Seminary News Updates"
    link = "/news/rss"
    description = "Latest news from the Consolata"

    def items(self):
        return NewsArticle.objects.order_by('-date_added')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.content[:200]
    
    def item_link(self, item):
        return reverse ("blogs:news_detail", args=[item.id])