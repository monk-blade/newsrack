#!/usr/bin/env python
# vim:fileencoding=utf-8
from datetime import datetime, timedelta

from calibre.utils.date import parse_date
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree
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
    use_embedded_content = False
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}

    extra_css = '''
        #img-cap, .ie-authorbox, .author-block, #storycenterbyline { font-size:small; }
        blockquote { color:#404040; }
        em, #sub-d { color:#202020; font-style:italic; }
        img { display:block; margin:0 auto; }
    '''
    remove_tags_after = [
        dict(name='div', attrs={'class': 'ev-meter-content'})
    ]
    resolve_internal_links = True
    remove_empty_feeds = True
    compress_news_images = True
    compress_news_images_auto_size = 16
    scale_news_images = (800, 600)
    keep_only_tags = [classes('heading-part full-details')]
    remove_tags = [
        dict(name='div', attrs={'id': 'ie_story_comments'}),
        dict(name='div', attrs={'class': lambda x: x and 'related-widget' in x}),
        dict(name='img', attrs={'src':lambda x: x and x.endswith('-button-300-ie.jpeg')}),
        dict(name='a', attrs={'href':lambda x: x and x.endswith('/?utm_source=newbanner')}),
        classes(
            'share-social appstext ie-int-campign-ad ie-breadcrumb custom_read_button unitimg copyright '
            'storytags pdsc-related-modify news-guard premium-story append_social_share ie-int-campign-ad '
            'digital-subscriber-only h-text-widget ie-premium ie-first-publish adboxtop adsizes immigrationimg '
            'next-story-wrap ie-ie-share next-story-box brand-logo quote_section ie-customshare osv-ad-class '
            'custom-share o-story-paper-quite ie-network-commenting audio-player-tts-sec o-story-list subscriber_hide '
            'author-social author-follow author-img premium_widget_below_article'
        )
    ]

    def parse_index(self):

        section_list = [
            ('Daily Briefing', 'https://indianexpress.com/section/live-news/'),
            ('Front Page', 'https://indianexpress.com/print/front-page/'),
            ('India', 'https://indianexpress.com/section/india/'),
            # ('Express Network', 'https://indianexpress.com/print/express-network/'),
            ('Delhi Confidential', 'https://indianexpress.com/section/delhi-confidential/'),
            ('Opinion', 'http://indianexpress.com/section/opinion/'),
            ('UPSC-CSE Key', 'https://indianexpress.com/section/upsc-current-affairs/'),
            ('Explained', 'https://indianexpress.com/section/explained/'),
            ('Business', 'https://indianexpress.com/section/business/'),
            # ('Political Pulse', 'https://indianexpress.com/section/political-pulse/'),
            ('Sunday Eye', 'https://indianexpress.com/section/express-sunday-eye/'),
            ('World', 'https://indianexpress.com/section/world/'),
            # ('Education', 'https://indianexpress.com/section/education/'),
            # ('Gadgets', 'https://indianexpress.com/section/technology/gadgets/'),
            ('Tech Review', 'https://indianexpress.com/section/technology/tech-reviews/'),
            # ('Techhook', 'https://indianexpress.com/section/technology/techook/'),
            # ('Laptops', 'https://indianexpress.com/section/technology/laptops/'),
            # ('Mobiles & Tabs', 'https://indianexpress.com/section/technology/mobile-tabs/'),
            ('Science', 'https://indianexpress.com/section/technology/science/'),
            ('Movie Review', 'https://indianexpress.com/section/entertainment/movie-review/'),
        ]

        feeds = []

        # For each section title, fetch the article urls
        for section in section_list:
            section_title = section[0]
            section_url = section[1]
            self.log(section_title, section_url)
            soup = self.index_to_soup(section_url)
            if '/world/' in section_url or '/explained/' in section_url:
                articles = self.articles_from_page(soup)
            else:
                articles = self.articles_from_soup(soup)
            if articles:
                feeds.append((section_title, articles))
        return feeds

    def articles_from_page(self, soup):
        ans = []
        for div in soup.findAll(attrs={'class':['northeast-topbox', 'explained-section-grid']}):
            for a in div.findAll('a', href=True):
                if not a.find('img') and '/section/' not in a['href']:
                    url = a['href']
                    title = self.tag_to_string(a)
                    self.log('\t', title, '\n\t\t', url)
                    ans.append({'title': title, 'url': url, 'description': ''})
        return ans

    def articles_from_soup(self, soup):
        ans = []
        div = soup.find('div', attrs={'class':['nation', 'o-opin']})
        for art in div.findAll(attrs={'class':['articles', 'o-opin-article']}):
            for a in art.findAll('a', href=True):
                if not a.find('img') and not ('/profile/' in a['href'] or '/agency/' in a['href']):
                    url = a['href']
                    title = self.tag_to_string(a)
                    desc = ''
                    if p:= art.find('p'):
                        desc = self.tag_to_string(p)
                    if da := art.find('div', attrs={'class':['date', 'o-opin-date']}):
                        date = parse_date(self.tag_to_string(da)).replace(tzinfo=None)
                        today = datetime.now()
                        if (today - date) > timedelta(self.oldest_article):
                            continue
                    self.log('\t', title, '\n\t', desc, '\n\t\t', url)
                    ans.append({'title': title, 'url': url, 'description': desc})
        return ans

    def get_cover_url(self):
        soup = self.index_to_soup(
            'https://www.readwhere.com/newspaper/indian-express/Nagpur/38726'
        )
        citem = soup.find('meta', attrs={'property':'og:image'})
        return citem['content'].replace('300', '600')

    def preprocess_html(self, soup):
        if h2 := soup.find('h2'):
            h2.name = 'p'
            h2['id'] = 'sub-d'
        for span in soup.findAll(
            'span', attrs={'class': ['ie-custom-caption', 'custom-caption']}
        ):
            span['id'] = 'img-cap'
        for img in soup.findAll('img'):
            noscript = img.findParent('noscript')
            if noscript is not None:
                lazy = noscript.findPreviousSibling('img')
                if lazy is not None:
                    lazy.extract()
                noscript.name = 'div'
        if span := soup.find('span', content=True, attrs={'itemprop':'dateModified'}):
            date = parse_date(span['content']).replace(tzinfo=None)
            today = datetime.now()
            if (today - date) > timedelta(self.oldest_article):
                self.abort_article('Skipping old article')
        return soup

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