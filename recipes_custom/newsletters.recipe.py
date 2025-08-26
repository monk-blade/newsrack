#!/usr/bin/env  python

import time
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime
_name = 'Newsletters'

class Newsletters(BasicNewsRecipe):
    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    description = 'My Favourite Newsletters from Substack.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 2 # days
    encoding = 'utf-8'
    use_embedded_content = True
    simultaneous_downloads = 9
    #masthead_url = 'https://upload.wikimedia.org/wikipedia/en/0/06/Sandesh%28IndianNewspaper%29Logo.jpg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """

    feeds = [
        ('The Core', 'https://rss.beehiiv.com/feeds/4BOnz8D132.xml'),
        ('The Daily Brief by Zerodha', 'https://thedailybrief.zerodha.com/feed'),
        ('Masala Chai', 'https://rss.beehiiv.com/feeds/Jk0t0xwJeq.xml'),
        ('Public Policy' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=f781f37f49c75d5e12d31bf2610d0d54&f=rss'),
        ('India Wants to Know', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=5d2a22d418134e27d410bac251a9e307&f=rss'),
        # ('Multitudes' ,'https://shantanukishwar.substack.com/feed'),
        # ('Wisdom Project', 'https://wisdomproject.substack.com/feed'),
        # ('Bank on Basak', 'https://www.bankonbasak.com/feed'),
        # ('Curated Commons', 'https://subbu.substack.com/feed'),
        # ('Environment of India', 'https://www.environmentofindia.com/feed'),
        ]