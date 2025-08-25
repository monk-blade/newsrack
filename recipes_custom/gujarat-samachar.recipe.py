#!/usr/bin/env  python
from datetime import date  # Correct import
from datetime import datetime
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree

_name = 'News of Gujarat'
class GujaratSamachar(BasicNewsRecipe):
    title = 'News of Gujarat'
    description = 'News of Gujarat is compilation of various feeds of Gujarati Paper'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 1.25  # days
    max_articles_per_feed = 50
    summary_length = 175
    publication_type = "newspaper"
    encoding = 'utf-8'
    center_navbar = True
    use_embedded_content = True
    masthead_url = 'https://www.gujaratsamachar.com/assets/logo.png'
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
        ('Sandesh | Opinion', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=a2abf353cf0a8c508fb6c10f36856ad9&f=rss'),
        ('GS | Editorials', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=93efd7f00ba0514c11e60494b70edd44&f=rss'),
        ('ઓરિજનલ | દિવ્યભાસ્કર', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=7a0609bc4ecc4fbadaf1c9c831ac62a1&f=rss'),
        ('ગુજરાતી પૂર્તિઓ' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=6d573adee7f766e07d3cbd8b8d4fee40&f=rss'),
        # ('Multitudes' ,'https://shantanukishwar.substack.com/feed'),
        # ('India Wants to Know', 'https://iwtkquiz.substack.com/feed'),
        # ('Wisdom Project', 'https://wisdomproject.substack.com/feed'),
        # ('Bank on Basak', 'https://www.bankonbasak.com/feed'),
        # ('Curated Commons', 'https://subbu.substack.com/feed'),
        # ('Environment of India', 'https://www.environmentofindia.com/feed'),
        ]
