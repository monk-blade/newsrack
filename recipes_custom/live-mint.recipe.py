#!/usr/bin/env python
# vim:fileencoding=utf-8
import json
import re
from datetime import date
from datetime import datetime  # Correct import

from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'

class LiveMint(BasicNewsRecipe):
    title = 'Live Mint - ' + datetime.now().strftime('%d.%m.%Y')
    description = 'Financial News from India.'
    language = 'en_IN'
    __author__ = 'Krittika Goyal, revised by unkn0wn'
    oldest_article = 1  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = False
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    masthead_url = 'https://images.livemint.com/static/livemint-logo-v1.svg'

    recipe_specific_options = {
        'days': {
            'short': 'Oldest article to download from this news source. In days ',
            'long': 'For example, 0.5, gives you articles from the past 12 hours',
            'default': str(oldest_article)
        }
    }
    remove_empty_feeds = True
    resolve_internal_links = True
    is_saturday = date.today().weekday() == 5

    def __init__(self, *args, **kwargs):
        BasicNewsRecipe.__init__(self, *args, **kwargs)
        d = self.recipe_specific_options.get('days')
        if d and isinstance(d, str):
            self.oldest_article = float(d)

    def get_cover_url(self):
        soup = self.index_to_soup('https://epaper.livemint.com/')
        cov = soup.findAll('img', attrs={'src': lambda x: x and x.startswith('/EPAPERIMAGES')})
        for x in cov:
            if 'MINT_FRONT_1' in x['src']:
                return 'https://epaper.livemint.com' + x['src'].replace('-S', '')

    if is_saturday:
        title = 'Mint Lounge'
        masthead_url = 'https://lifestyle.livemint.com/mintlounge/static-images/lounge-logo.svg'

        oldest_article = 6.5 # days

        extra_css = '''
            #story-summary-0 {font-style:italic; color:#202020;}
            .innerBanner, .storyImgSec {text-align:center; font-size:small;}
            .author {font-size:small;}
        '''

        keep_only_tags = [
            classes('storyPageHeading storyContent innerBanner author')
        ]
        remove_tags = [
            dict(name=['meta', 'link', 'svg', 'button', 'iframe']),
            classes('hidden-article-url sidebarAdv similarStoriesClass moreFromSecClass linkStories publishDetail'),
            dict(attrs={'id':['hidden-article-id-0', 'hidden-article-type-0']})
        ]

        feeds = [
            ('Lounge News', 'https://lifestyle.livemint.com/rss/news'),
            ('Food', 'https://lifestyle.livemint.com/rss/food'),
            ('Fashion', 'https://lifestyle.livemint.com/rss/fashion'),
            ('How to Lounge', 'https://lifestyle.livemint.com/rss/how-to-lounge'),
            ('Smart Living', 'https://lifestyle.livemint.com/rss/smart-living'),
            ('Health', 'https://lifestyle.livemint.com/rss/health'),
            ('Relationships', 'https://lifestyle.livemint.com//rss/relationships')
        ]

        def preprocess_html(self, soup):
            if h2 := soup.find('h2'):
                h2.name = 'p'
            for also in soup.findAll('h2'):
                if self.tag_to_string(also).strip().startswith('Also'):
                    also.extract()
            for img in soup.findAll('img', attrs={'data-img': True}):
                img['src'] = img['data-img']
            return soup
    else:

        extra_css = '''
            img {margin:0 auto;}
            .psTopLogoItem img, .ecologoStory { width:100; }
            #img-cap {font-size:small; text-align:center;}
            .summary, .highlights, .synopsis {
                font-weight:normal !important; font-style:italic; color:#202020;
            }
            em, blockquote {color:#202020;}
            .moreAbout, .articleInfo, .metaData, .psTopicsHeading, .topicsTag, .auth {font-size:small;}
        '''

        keep_only_tags = [
            dict(name='article', attrs={'id':lambda x: x and x.startswith(('article_', 'box_'))}),
            dict(attrs={'class':lambda x: x and x.startswith('storyPage_storyBox__')}),
            classes('contentSec')
        ]
        remove_tags = [
            dict(name=['meta', 'link', 'svg', 'button', 'iframe']),
            dict(attrs={'class':lambda x: x and x.startswith(
                ('storyPage_alsoRead__', 'storyPage_firstPublishDate__', 'storyPage_bcrumb__')
            )}),
            dict(attrs={'id':['faqSection', 'seoText', 'ellipsisId']}),
            classes(
                'trendingSimilarHeight moreNews mobAppDownload label msgError msgOk taboolaHeight gadgetSlider ninSec'
                ' socialHolder imgbig disclamerText disqus-comment-count openinApp2 lastAdSlot bs_logo author-widget'
                ' datePublish sepStory premiumSlider moreStory Joinus moreAbout milestone benefitText checkCibilBtn trade'
            )
        ]

        feeds = [
            ('Companies', 'https://www.livemint.com/rss/companies'),
            ('Opinion', 'https://www.livemint.com/rss/opinion'),
            ('Money', 'https://www.livemint.com/rss/money'),
            ('Economy', 'https://www.livemint.com/rss/economy'),
            ('Politics', 'https://www.livemint.com/rss/politics'),
            ('Science', 'https://www.livemint.com/rss/science'),
            ('Industry', 'https://www.livemint.com/rss/industry'),
            ('Education', 'https://www.livemint.com/rss/education'),
            ('Sports', 'https://www.livemint.com/rss/sports'),
            ('Technology', 'https://www.livemint.com/rss/technology'),
            ('News', 'https://www.livemint.com/rss/news'),
            ('Mutual Funds', 'https://www.livemint.com/rss/Mutual Funds'),
            ('Markets', 'https://www.livemint.com/rss/markets'),
            ('AI', 'https://www.livemint.com/rss/AI'),
            ('Insurance', 'https://www.livemint.com/rss/insurance'),
            ('Budget', 'https://www.livemint.com/rss/budget'),
            # ('Elections', 'https://www.livemint.com/rss/elections'),
        ]

        def preprocess_raw_html(self, raw, *a):
            # remove empty p tags
            raw = re.sub(
                r'(<p>\s*)(<[^(\/|a|i|b|em|strong)])', '\g<2>', re.sub(
                    r'(<p>\s*&nbsp;\s*<\/p>)|(<p>\s*<\/p>)|(<p\s*\S+>&nbsp;\s*<\/p>)', '', raw
                )
            )
            if '<script>var wsjFlag=true;</script>' in raw:
                m = re.search(r'type="application/ld\+json">[^<]+?"@type": "NewsArticle"', raw)
                raw1 = raw[m.start():]
                raw1 = raw1.split('>', 1)[1].strip()
                data = json.JSONDecoder().raw_decode(raw1)[0]
                value = data['hasPart']['value']
                body = data['articleBody'] + '</p> <p>'\
                        + re.sub(r'(([a-z]|[^A-Z])\.|\.”)([A-Z]|“[A-Z])', r'\1 <p> \3', value)
                body = '<div class="FirstEle"> <p>' +  body  + '</p> </div>'
                raw2 = re.sub(r'<div class="FirstEle">([^}]*)</div>', body, raw)
                return raw2
            return raw

        def preprocess_html(self, soup):
            for h2 in soup.findAll('h2'):
                h2.name = 'h4'
            auth = soup.find(attrs={'class':lambda x: x and x.startswith(('storyPage_authorInfo__', 'storyPage_authorSocial__'))})
            if auth:
                auth['class'] = 'auth'
            summ = soup.find(attrs={'class':lambda x: x and x.startswith('storyPage_summary__')})
            if summ:
                summ['class'] = 'summary'
            for strong in soup.findAll('strong'):
                if strong.find('p'):
                    strong.name = 'div'
            for embed in soup.findAll('div', attrs={'class':'embed'}):
                nos = embed.find('noscript')
                if nos:
                    nos.name = 'span'
            for span in soup.findAll('figcaption'):
                span['id'] = 'img-cap'
            for auth in soup.findAll('span', attrs={'class':lambda x: x and 'articleInfo' in x.split()}):
                auth.name = 'div'
            for img in soup.findAll('img', attrs={'data-src': True}):
                img['src'] = img['data-src']
            for span in soup.findAll('span', attrs={'class':'exclusive'}):
                span.extract()
            for al in soup.findAll('a', attrs={'class':'manualbacklink'}):
                pa = al.findParent(['p', 'h2', 'h3', 'h4'])
                if pa:
                    pa.extract()
            wa = soup.find(**classes('autobacklink-topic'))
            if wa:
                p = wa.findParent('p')
                if p:
                    p.extract()
            return soup

        def populate_article_metadata(self, article, soup, first):
            article.title = article.title.replace('<span class="webrupee">₹</span>','₹')


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
                    h2_tag = tree.xpath('//h1')
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