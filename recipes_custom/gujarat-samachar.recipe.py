#!/usr/bin/env  python
from datetime import date  # Correct import
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree

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

    def postprocess_book(self, oeb, opts, log):
        # Iterate over each item in the manifest
        for item in oeb.manifest.items:
            log.info(f"File Name: {item.href}")
            if item.media_type == 'text/html':
                # Access the content of the item
                soup = item.data
                # Ensure soup is an lxml element
                if isinstance(soup, etree._Element):
                    # Convert the lxml element to a string for processing
                    html_content = etree.tostring(soup, pretty_print=True, encoding='unicode')
                    # Parse the HTML content with lxml
                    parser = etree.HTMLParser()
                    tree = etree.fromstring(html_content, parser)
                    
                    # Find all <p> tags using XPath
                    p_tags = tree.xpath('//p')
                    
                    # Iterate through the <p> tags
                    for p in p_tags:
                        # Check if the <p> tag contains the specified string
                        if "This article was downloaded by" in ''.join(p.xpath('.//text()')):
                            # Remove the <p> tag from the HTML content
                            p.getparent().remove(p)
                    
                    # Find the h2 tag and the div with class calibre_navbar1 using XPath
                    h2_tag = tree.xpath('//h2')
                    div_tag = tree.xpath('//div[@class="calibre_navbar"]')
                    
                    if h2_tag and div_tag:
                        h2_tag = h2_tag[0]
                        div_tag = div_tag[0]
                        # Get the parent of both tags
                        parent = h2_tag.getparent()
                        # Ensure both elements have the same parent
                        if parent == div_tag.getparent():
                            # Remove both tags from the parent
                            parent.remove(h2_tag)
                            parent.remove(div_tag)
                            # Reinsert the tags in the desired order
                            parent.insert(0, h2_tag)
                            parent.insert(1, div_tag)
                    
                    # Convert the modified tree back to a string
                    modified_html = etree.tostring(tree, pretty_print=True, encoding='unicode')
                    # Parse the modified HTML back to an lxml element
                    soup = etree.fromstring(modified_html)
                    
                    # Update the item data with the modified HTML content
                    item.data = soup
                else:
                    log.error("The soup object is not an lxml element.")

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'