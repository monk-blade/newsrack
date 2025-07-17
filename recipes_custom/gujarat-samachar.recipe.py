#!/usr/bin/env  python
from datetime import date  # Correct import
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree

_name = 'Gujarat Samachar'
class GujaratSamachar(BasicNewsRecipe):
    title = u'News of Gujarat- ' + datetime.now().strftime('%d.%m.%Y')
    description = 'News of Gujarat is compilation of various feeds of Gujarati Paper'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 2  # days
    max_articles_per_feed = 50
    summary_length = 175
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
        ('Gujarati OpEd', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=f812f5337e58e666b5b0b4050475ba44&f=rss'),
        ('ગુજરાતી પૂર્તિઓ' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=6d573adee7f766e07d3cbd8b8d4fee40&f=rss'),
        # ('Multitudes' ,'https://shantanukishwar.substack.com/feed'),
        # ('India Wants to Know', 'https://iwtkquiz.substack.com/feed'),
        # ('Wisdom Project', 'https://wisdomproject.substack.com/feed'),
        # ('Bank on Basak', 'https://www.bankonbasak.com/feed'),
        # ('Curated Commons', 'https://subbu.substack.com/feed'),
        # ('Environment of India', 'https://www.environmentofindia.com/feed'),
        ]
