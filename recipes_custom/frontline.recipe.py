#!/usr/bin/env python
# vim:fileencoding=utf-8
from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Frontline'

class Frontline(BasicNewsRecipe):
    title = u'Frontline'
    __author__ = 'unkn0wn'
    description = 'Frontline, the fortnightly English magazine from the stable of The Hindu, has been a distinguished presence in the media world since 1984.'
    language = 'en_IN'
    no_stylesheets = True
    remove_javascript = True
    use_embedded_content = False
    encoding = 'utf-8'
    oldest_article = 14
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    max_articles_per_feed = 50
    ignore_duplicate_articles = {'url'}
    # masthead_url = 'https://fl.thgim.com/static/theme/default/base/img/fllogo.png'
    remove_attributes = ['height', 'width']

    def get_cover_url(self):
        soup = self.index_to_soup(
            'https://frontline.thehindu.com/current-issue/')
        tag = soup.find(attrs={'class': 'sptar-image'})
        if tag:
            self.cover_url = tag.find('img')['data-original']
        return super().get_cover_url()

    # https://fl.thgim.com/incoming/b5zy2g/article38454943.ece/alternates/FREE_100/coverpng

    keep_only_tags = [
        classes(
            'overline mainart-title marginBottom10px articleBottomLine swiper-slide slide-caption artlead-text body-main article-container'
        )
    ]
    remove_tags = [classes('dispatche-middle bigtitle mobilesocialicons ece_frontpage shareicon-article')]

    remove_tags_after = [
        classes('body-main'),
    ]


    extra_css = """
    .lead-img-caption { font-size: 0.8rem; color: #c7c7c7; }
    p{text-align: justify; font-size: 100%}
    """


    feeds = [
        ('Cover Story',
         'https://frontline.thehindu.com/cover-story/feeder/default.rss'),
        ('The Nation',
         'https://frontline.thehindu.com/the-nation/feeder/default.rss'),
        ('World Affairs',
         'https://frontline.thehindu.com/world-affairs/feeder/default.rss'),
        ('Politics',
         'https://frontline.thehindu.com/politics/feeder/default.rss'),
        ('Arts & Culture',
         'https://frontline.thehindu.com/arts-and-culture/feeder/default.rss'),
        ('Social Issues',
         'https://frontline.thehindu.com/social-issues/feeder/default.rss'),
        ('Books', 'https://frontline.thehindu.com/books/feeder/default.rss'),
        ('Columns',
         'https://frontline.thehindu.com/columns/feeder/default.rss'),
        ('Others', 'https://frontline.thehindu.com/other/feeder/default.rss'),
    ]

    def preprocess_html(self, soup):
        for source in soup.findAll('source', srcset=True, attrs={'media':'(min-width: 1600px)'}):
            source.name = 'img'
            source['src'] = source['srcset']
        for img in soup.findAll('img', attrs={'data-original':True}):
            img['src'] = img['data-original']
        return soup
