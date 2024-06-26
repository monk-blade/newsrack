#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes


class OpenMagazine(BasicNewsRecipe):
    title = u'Open Magazine'
    description = 'The weekly current affairs and features magazine.'
    language = 'en_IN'
    __author__ = 'unkn0wn'
    oldest_article = 7  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    use_embedded_content = False
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    masthead_url = 'https://openthemagazine.com/wp-content/themes/open/images/logo.png'
    ignore_duplicate_articles = {'url'}
    extra_css = """
            p{text-align: justify; font-size: 100%}
            blockquote{color:#404040;}
            {font-size: small;font-style: italic;}
            .about-author{font-size:small;}
            [id^="caption-attachment"]
    """
    def get_cover_url(self):
        soup = self.index_to_soup('https://openthemagazine.com/magazine/')
        tag = soup.find(attrs={'class': 'mb-2 right-image'})
        if tag:
            self.cover_url = tag.find('img')['data-src']
        return super().get_cover_url()

    keep_only_tags = [
        classes('post-data post-thumb post-meta post-excerp'),
    ]

    remove_tags = [
        classes('top-social menu-social post-author blurb-social button-links'),
    ]

    remove_tags_after = [
        classes('post-meta post-excerp'),
    ]

    feeds = [
        ('Cover Story', 'https://openthemagazine.com/cover-story/feed/'),
        ('Columns', 'https://openthemagazine.com/columns/feed'),
        ('Essays', 'https://openthemagazine.com/essays/feed'),
        ('Features', 'https://openthemagazine.com/features/feed'),
        ('Books', 'https://openthemagazine.com/lounge/books/feed'),
        ('Art & Culture', 'https://openthemagazine.com/art-culture/feed'),
        ('Cinema', 'https://openthemagazine.com/cinema/feed'),
    ]
    def preprocess_html(self, soup):
        for img in soup.findAll('img', attrs={'data-src':True}):
            img['src'] = img['data-src']
        return soup
