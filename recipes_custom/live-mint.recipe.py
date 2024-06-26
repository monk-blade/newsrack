#!/usr/bin/env  python
import json
import re
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import date

_name = "Live Mint"

is_saturday = date.today().weekday() == 5


class LiveMint(BasicNewsRecipe):
    title = u'Live Mint'
    description = 'Financial News from India.'
    language = 'en_IN'
    __author__ = 'Krittika Goyal'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    no_stylesheets = True
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    remove_attributes = ['style', 'height', 'width']
    remove_empty_feeds =  True
    extra_css = """
        .highlights{font-style: italic; font-size: medium; font-weight: bold; margin: 0;background: #eee; padding: 1em; border-radius: 0.5em; list-style:none}
        picture+div{font-size: small;display: block;font-weight: bold;margin:0.4em;}
        span.author::before{content: " - ";}
        #img-cap {font-size:small; text-align:center;}
        #auth-info {font-size:small; text-align:center;}
        .summary{font-style:italic; color:#404040;}
        .articleInfo{display: inline-block; padding:0.4em; color:gray; font-size:small;}
        p{text-align: justify; font-size: 100%}
    """
    if is_saturday:
        keep_only_tags = [
            dict(name='h1'),
            dict(name='h2', attrs={'id':'story-summary-0'}),
            dict(name='picture'),
            dict(name='div', attrs={'class':'innerBanCaption'}),
            dict(name='div', attrs={'id':'date-display-before-content'}),
            dict(name='div', attrs={'class':'storyContent'}),
        ]
        remove_tags = [
            classes(
                'trendingSimilarHeight moreNews mobAppDownload label msgError msgOk exclusive disclamerText outsideSso disqus-comment-count moreAbout'
            ),
            dict(name='p', attrs={'class':'summary'})
        ]
        feeds = [
            ('News', 'https://lifestyle.livemint.com/rss/news'),
            ('Food','https://lifestyle.livemint.com/rss/food'),
            ('Fashion','https://lifestyle.livemint.com/rss/fashion'),
            ('How to Lounge','https://lifestyle.livemint.com/rss/how-to-lounge'),
            ('Smart Living','https://lifestyle.livemint.com/rss/smart-living'),
        ]

        def preprocess_html(self, soup):
            for img in soup.findAll('img', attrs={'data-img': True}):
                img['src'] = img['data-img']
            return soup
    else:
        keep_only_tags = [
            dict(name='h1'),
            dict(name='picture'),
            dict(name='figcaption'),
            dict(name='figure', attrs={'data-vars-mediatype':'image'}),
            classes('articleInfo FirstEle summary highlights paywall'),
        ]
        remove_tags = [
            classes(
                'trendingSimilarHeight moreNews mobAppDownload label msgError msgOk exclusive disclamerText outsideSso disqus-comment-count moreAbout'
                ' socialHolder imgbig disclamerText disqus-comment-count taboolaHeight'
            ),
            dict(name='p', attrs={'class':'summary'})
        ]

        feeds = [
            ('Economy', 'https://www.livemint.com/rss/economy/'),
            ('Politics', 'https://www.livemint.com/rss/politics'),
            ('Science', 'https://www.livemint.com/rss/science'),
            ('Opinion', 'https://www.livemint.com/rss/opinion'),
            ('Money', 'https://www.livemint.com/rss/money'),
            ('News', 'https://www.livemint.com/rss/news'),
            ('Markets', 'https://www.livemint.com/rss/markets'),
            ('Companies', 'https://www.livemint.com/rss/companies'),
            ('Industry', 'https://www.livemint.com/rss/industry'),
            ('Education', 'https://www.livemint.com/rss/education'),
            ('Sports', 'https://www.livemint.com/rss/sports'),
            ('Technology', 'https://www.livemint.com/rss/technology'),
            ('Insurance', 'https://www.livemint.com/rss/insurance'),
            ('Budget', 'https://www.livemint.com/rss/budget'),
            ('Elections', 'https://www.livemint.com/rss/elections'),
        ]
        def preprocess_raw_html(self, raw, *a):
            if '<script>var wsjFlag=true;</script>' in raw:
                m = re.search(r'type="application/ld\+json">[^<]+?"@type": "NewsArticle"', raw)
                raw1 = raw[m.start():]
                raw1 = raw1.split('>', 1)[1].strip()
                data = json.JSONDecoder().raw_decode(raw1)[0]
                value = data['hasPart']['value']
                body = data['articleBody'] + '</p> <p>'\
                        + re.sub(r'(([a-z]|[^A-Z])\.|\.”)([A-Z]|“[A-Z])', r'\1 <p> \3', value)
                body = '<div class="FirstEle"> <p>' +  body  + '</p> </div>'
                raw = re.sub(r'<div class="FirstEle">([^}]*)</div>', body, raw)
                return raw
            else:
                return raw

        def preprocess_html(self, soup):
            for span in soup.findAll('figcaption'):
                span['id'] = 'img-cap'
            for auth in soup.findAll('span', attrs={'class':['articleInfo pubtime','articleInfo author']}):
                auth['id'] = 'auth-info'
                auth.name = 'div'
            for span in soup.findAll('span', attrs={'class':'exclusive'}):
                span.extract()
            for img in soup.findAll('img', attrs={'data-src': True}):
                img['src'] = img['data-src']
            return soup

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'