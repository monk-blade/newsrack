__license__ = 'GPL v3'
__copyright__ = '2009-2012, Darko Miletic <darko.miletic at gmail.com>'
'''
www.business-standard.com
'''

from calibre.web.feeds.recipes import BasicNewsRecipe

_name = 'Business Standard'

def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


class BusinessStandard(BasicNewsRecipe):
    title = 'Business Standard'
    __author__ = 'Darko Miletic'
    description = "India's most respected business daily"
    oldest_article = 1
    max_articles_per_feed = 20
    no_stylesheets = True
    use_embedded_content = False
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    encoding = 'utf-8'
    publisher = 'Business Standard Limited'
    category = 'news, business, money, india, world'
    language = 'en_IN'

    masthead_url = 'https://bsmedia.business-standard.com/include/_mod/site/html5/images/business-standard-logo.png'

    def get_cover_url(self):
        soup = self.index_to_soup('https://www.magzter.com/IN/Business-Standard-Private-Ltd/Business-Standard/Newspaper/')
        for citem in soup.findAll('meta', content=lambda s: s and s.endswith('view/3.jpg')):
            return citem['content']

    remove_attributes = ['width', 'height', 'style']

    keep_only_tags = [
            classes('headline alternativeHeadline full-img article-content__img pubDate'),
            dict(name='span', attrs={'class':'p-content'}),
    ]
    remove_tags = [
            classes('also-read-panel'),
            dict(name='p', attrs={'id':'auto_disclaimer'}),

    ]
    extra_css = """
            h2 { font-size: medium; font-weight: bold;}
            .pubDate {font-size: small; color: gray;}
            .full-img {float: left; clear: both; font-style:italic; padding: 10px 10px 10px 0px;}
            p{text-align: justify; font-size: 100%}
    """

    feeds = [
        (u'Economy and Policy', u'https://www.business-standard.com/rss/economy-policy-102.rss'),
        (u'Finance', u'https://www.business-standard.com/rss/finance-103.rss'),
        (u'Beyond Business', u'https://www.business-standard.com/rss/beyond-business-104.rss'),
        (u'Opinion', 'https://www.business-standard.com/rss/opinion-105.rss'),
        (u'Markets', u'https://www.business-standard.com/rss/markets-106.rss'),
        (u'Technology', u'https://www.business-standard.com/rss/technology-108.rss'),
        (u'Companies', u'https://www.business-standard.com/rss/companies-101.rss'),
        (u'Personal Finance', u'https://www.business-standard.com/rss/pf-114.rss'),
        (u'International', u'https://www.business-standard.com/rss/international-116.rss'),
        # (u'Today\'s Paper', u'https://www.business-standard.com/rss/todays-paper.rss'),
        # for todays paper - subscrition required
    ]
