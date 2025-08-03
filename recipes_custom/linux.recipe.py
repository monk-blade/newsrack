#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime
_name = 'Linux'

class Linux(BasicNewsRecipe):
    title = _name + u' - ' + datetime.now().strftime('%d.%m.%Y')
    description = 'My Favourite linux website feeds.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 1  # days
#     max_articles_per_feed = 1
    encoding = 'utf-8'
    use_embedded_content = True
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
        ('OMG! Ubuntu', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=03286255647546a832597c8c99addfa8&f=rss'),
        ('Phoronix' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=2bab43c9dbc153cd7c03ab979ff6c2bf&f=rss'),
        ('This Week in GNOME' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=edde32a423219f4ee7d31f1e06be04c0&f=rss'),
        ('Adventures in KDE', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=477c3220ee5a498a9de1fe5ad2b3ed01&f=rss'),
        ('Announcements | nixOS', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=f5871e449b44927a088b5180c5b3d89f&f=rss'),
        # ('Bank on Basak', 'https://www.bankonbasak.com/feed'),
        # ('Curated Commons', 'https://subbu.substack.com/feed'),
        # ('Environment of India', 'https://www.environmentofindia.com/feed'),
        ]

#        ('Network Capital', 'https://www.thenetworkcapital.com/feed'),       
#        https://pradologue.substack.com/feed
