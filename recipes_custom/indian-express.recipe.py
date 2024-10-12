#!/usr/bin/env python
# vim:fileencoding=utf-8
from datetime import datetime, timedelta

from calibre.utils.date import parse_date
from calibre.web.feeds.news import BasicNewsRecipe, classes


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