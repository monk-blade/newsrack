#!/usr/bin/env python
# vim:fileencoding=utf-8

from calibre.web.feeds.news import BasicNewsRecipe, classes

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
class IndianExpress(BasicNewsRecipe):
    title = u'Indian Express'
    language = 'en_IN'
    __author__ = 'unkn0wn'
    oldest_article = 1.15  # days
    max_articles_per_feed = 25
    encoding = 'utf-8'
    masthead_url = 'https://indianexpress.com/wp-content/themes/indianexpress/images/indian-express-logo-n.svg'
    no_stylesheets = True
    use_embedded_content = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    extra_css = '''
        #img-cap, .ie-authorbox, .author-block, #storycenterbyline { font-size:small; }
        blockquote { color:#404040; }
        em, #sub-d { color:#202020; font-style:italic; }
        img { display:block; margin:0 auto; }
    '''   
    feeds = [
        ('IE Explained', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=870ee7e79a574c5f83ac21ac1998ed54&f=rss'),
        # ('Public Policy' ,'https://publicpolicy.substack.com/feed'),
        # ('Multitudes' ,'https://shantanukishwar.substack.com/feed'),
        # ('India Wants to Know', 'https://iwtkquiz.substack.com/feed'),
        # ('Wisdom Project', 'https://wisdomproject.substack.com/feed'),
        # ('Bank on Basak', 'https://www.bankonbasak.com/feed'),
        # ('Curated Commons', 'https://subbu.substack.com/feed'),
        # ('Environment of India', 'https://www.environmentofindia.com/feed'),
        ]

#        ('Network Capital', 'https://www.thenetworkcapital.com/feed'),       
#        https://pradologue.substack.com/feed
