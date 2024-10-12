#!/usr/bin/env  python
import json
from datetime import date  # Correct import
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from mechanize import Request
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree

_name = 'Sandesh'
class Sandesh(BasicNewsRecipe):
    title = u'Sandesh'
    description = 'Sandesh is a Gujarati language daily newspaper in India.'
    language = 'gu'
    __author__ = 'Arpan'
    category = 'news, India'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    center_navbar = True
    use_embedded_content = True
    masthead_url = 'https://upload.wikimedia.org/wikipedia/en/0/06/Sandesh%28IndianNewspaper%29Logo.jpg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 16
    scale_news_images = (800, 600)
    feeds = [
    ('Gujarat' ,'https://sandesh.com/rss/gujarat.xml'),        
    ('National', 'https://sandesh.com/rss/india.xml'),
    ('International', 'https://sandesh.com/rss/world.xml'),
    ('Editorial', 'https://sandesh.com/rss/opinion.xml'),
    ('Science & Technology', 'https://sandesh.com/rss/tech.xml'),
    ('Business', 'https://sandesh.com/rss/business.xml'),
#        ('Sports', 'https://sandesh.com/rss/sports.xml'),
#        ('Health', 'https://sandesh.com/rss/health.xml'),
#        ('Lifestyle & Fashion', 'https://sandesh.com/rss/lifestyle.xml'),
#        ('Entertainment', 'https://sandesh.com/rss/entertainment.xml'),
    ]
    remove_tags = [
        classes('inner_ad inner_ag inner_ar allSubscribe cf'),
    #    dict(name='div', attrs={'id':'subs-popup-banner'}),
    #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
    ]

    extra_css = """
            h2 {
                text-align: center;
                margin: 0;
                font-size: 1.1em;
            }
            p {
                text-align: justify;
                margin: 0.25em !important;
            }
            .calibre_feed_title {
                text-align: center;
                padding: 0;
            }
            .calibre_navbar1 {
                text-align: center;
            }
            .calibre_navbar {
                text-align: center;
            }
    """
    template_css = """
            .article {
                font-size: 0.75em !important;
                font-weight: bold;
                line-height: 1 !important;
                text-align: left;
            }
            .article_date {
                color: gray;
                font-family: monospace;
                font-size: 5px;
            }
            .article_description {
                display: block;
                font-size: 5px;
                text-indent: 0;
            }
            .calibre_article_list {
                padding: 0;
                font-size: 0.75em;
            }
            .calibre_feed_description {
                display:none !important;
                margin: 0;
                padding:0;
                max-height: 0;
            }

    """
    # def postprocess_html(soup):
    #     print(soup)
    #     h2_tag = soup.find('h2')
    #     print("H2 tag:", h2_tag)
    #     #div_tag = soup.find('div')
    #     #print("DIV tag:", div_tag)
    #     return soup

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

    def parse_feeds(self):
        self.log(('Sandesh Feeds overrode parse_feeds()'))
        br = self.get_browser()
        parsed_feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in parsed_feeds:
            for article in feed.articles:
                # Remove 'https://sandesh.com' from article.url
                base_url = 'https://sandesh.com'
                if article.url.startswith(base_url):
                    path = article.url[len(base_url):]
                else:
                    path = article.url

                data = json.dumps({"url": path}).encode('utf-8')
                
                rq = Request(
                    url='https://new-wapi.sandesh.com/api/v1/post-details',
                    data=data,
                    headers={
                        'Accept': 'application/json, text/plain, */*',
                        'Origin': 'https://sandesh.com',
                        'Content-type': 'application/json;charset=UTF-8',
                        'url': path
                    },
                    method='POST'
                )
                try:
                    res = br.open(rq).read()
                    res = res.decode('utf-8')
                    res = json.loads(res)
                    #print("JSON Response:", res)  # Debug print to check JSON response
                    
                    # Extract data from JSON response
                    article_data = res.get('data', {})
                    tmp_img = article_data.get('media', '')
                    if(tmp_img):
                        img_url = "https://resize-img.sandesh.com/epapercdn.sandesh.com/" + tmp_img
                        img_data = "<img src='" + img_url + "'/>"
                    else:
                        img_data = ''
                    #print("Article Data:", article_data)  # Debug print to check article data
                    article.title = article_data.get('title', '')
                    article.content = img_data + article_data.get('content', '')
                    article.description = article_data.get('description', '')
                    article.date = article_data.get('publish_date', '')
                    article.author = article_data.get('byliner', '')
                    
                    # Debug prints to check if content is being set
                    #print("Article Content:", article.content)
                    #print("Article Description:", article.description)
                    #print("Article Date:", article.date)
                    #print("Article Author:", article.author)
                    
                    self.logged = True
                except Exception as e:
                    self.log.warn(f'\n**Request failed: {e}\n')
                    return br

        print(parsed_feeds)
        return parsed_feeds

    # def preprocess_html(self, soup):
    #     # Find the h2 and div tags
    #     #print(soup)
    #     h2_tag = soup.find('h2')
    #     div_tag = soup.findAll(**classes('calibre_navbar'))
    #     print("DIV tag" + div_tag.string)
    #     # Move the h2 tag before the div tag
    #     # if h2_tag and div_tag:
    #     #     div_tag.insert_after(h2_tag)
    #     return soup
    def get_cover_url(self):
        # Get today's date
        today = date.today()
        # Format the date in ddmmyyyy format
        formatted_date = today.strftime('%d%m%Y')
        self.cover_url = 'https://jionews.cdn.jio.com/jionewsdata/publicphp/' + formatted_date + '/Sandesh_Ahmedabad_933/1/thumb-1-new.jpg'
        return getattr(self, 'cover_url', self.cover_url)