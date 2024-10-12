#!/usr/bin/env  python
from datetime import date  # Correct import
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
#from mechanize import Request

_name = 'Gujarat Samachar'
class GujaratSamachar(BasicNewsRecipe):
    title = u'Gujarat Samachar'
    description = 'Gujarat Samachar is a Gujarati language daily newspaper in India.'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    center_navbar = True
    use_embedded_content = False
    masthead_url = 'https://www.gujaratsamachar.com/assets/logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    keep_only_tags = [
        classes('detail-news article-detail-news'),
    ]

    remove_tags = [
        classes('logo main-menu logo_date_time footer news-tags single-box social multiple citydrop react-share__ShareButton mx-1 breadcrumb noAfter border-0 card-header d-flex flex-wrap align-items-center'),
        dict(name='img', attrs={'src':'https://static.gujaratsamachar.com/content_image/content_image_6bd6b222-efb0-4f12-9bc6-6ad2a32fee11.jpeg'}),
    #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
     ]
    # remove_tags_after = [ classes('stry-bdy')]

    feeds = [
        ('Top Stories' ,'https://www.gujaratsamachar.com/rss/top-stories'),        
        ('National', 'https://www.gujaratsamachar.com/rss/category/national'),
        ('International', 'https://www.gujaratsamachar.com/rss/category/international'),
        ('Editorial', 'https://www.gujaratsamachar.com/rss/category/editorial'),
        ('Science & Technology', 'https://www.gujaratsamachar.com/rss/category/science-technology'),
        ('Business', 'https://www.gujaratsamachar.com/rss/category/business'),
 #       ('Sports', 'https://www.gujaratsamachar.com/rss/category/sports'),
 #       ('Health', 'https://www.gujaratsamachar.com/rss/category/health'),
#        ('Lifestyle & Fashion', 'https://www.gujaratsamachar.com/rss/category/lifestyle-fashion'),
#        ('Entertainment', 'https://www.gujaratsamachar.com/rss/category/entertainment'),
        ]

    extra_css = """
            .calibre-navbar {
                padding-top: 1em; 
            }
            h1 {
                text-align: center;
                margin: 0; /* Add padding for spacing */
                font-size: 1.2em;
            }
            p {
                text-align: justify;
                margin: 0.25rem; /* Reset margin for all <p> */
            }
            .article {
                font-size: 0.7em !important;
            }
            .article_date {
                font-size: 0.7em;
            }
            .calibre_feed_description {
                visibility: hidden;
                margin: 0;
                padding:0;
                font-size: 0em;
            }
            .calibre_feed_title {
                text-align: center;
                padding: 0;
            }
    """
    def get_cover_url(self):
        # Get today's date
        today = date.today()
        # Format the date in ddmmyyyy format
        formatted_date = today.strftime('%d%m%Y')
        self.cover_url = 'https://jionews.cdn.jio.com/jionewsdata/publicphp/' + formatted_date + '/Gujarat_Samachar_Rajkot_106/1/thumb-1-new.jpg'
        return getattr(self, 'cover_url', self.cover_url)
