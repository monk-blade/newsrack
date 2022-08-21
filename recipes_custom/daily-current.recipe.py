#!/usr/bin/env  python
#TODO fix image in 
from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Daily Current Affairs'

class dailycurrentaffairs(BasicNewsRecipe):
    title = _name
    description = 'My Daily Current Affairs feeds from populer UPSC Aspirant websites.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 1.5  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    #masthead_url = 'https://upload.wikimedia.org/wikipedia/en/0/06/Sandesh%28IndianNewspaper%29Logo.jpg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)

    keep_only_tags = [
        classes('card-body entry-content article-content content-area')
    ]

    remove_tags = [
        classes('printfriendly p-0 awac-wrapper mb-0 readmore blog addtoany_share_save_container wabtn_container content-box-red d-none entry-footer nav-tabs site-main'),
        dict(name = 'a', attrs = {'rel' : 'noopener'}),
        dict(name = 'blockquote', attrs = {'class' : 'wp-embedded-content'})
        # dict(name = 'div', attrs = {'id' : lambda x: x and x.startswith('inside_post_content_ad')}),    
        # dict(name = 'div', attrs = {'id' : lambda x: x and x.startswith('filler_ad')})
    ]

    feeds = [
        ('Civilsdaily','https://monk-blade.github.io/reader-scripts/rss.xml'),
        ('Insights', 'https://www.insightsonindia.com/category/current-affairs-2/feed/'),
        ('IASbaba', 'https://iasbaba.com/iasbabas-daily-current-affairs/feed/'),
        ('9PM Brief ForumIAS','https://blog.forumias.com/category/9-pm-brief/feed/'),
        ('Newspaper Clips', 'https://afeias.com/knowledge-centre/newspaper-clips/feed/'),
        ('7PM Editorial ForumIAS', 'https://blog.forumias.com/category/7-pm/feed/'),
        ]

#        ('Mains Marathon ForumIAS','https://blog.forumias.com/category/mains-marathon/feed/'),

    def preprocess_html(self, soup):
        for img in soup.findAll('img', attrs={'data-src': True}):
            img['src'] = img['data-src'].split('?')[0]
        return soup