from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime, timezone, timedelta
from calibre.utils.date import parse_date
import string

def absurl(x):
    if x.startswith('/'):
        x = 'https://www.livelaw.in' + x
    return x
    
class livelaw(BasicNewsRecipe):
    title = 'Live Law'
    __author__ = 'unkn0wn'
    description = (
        'Live Law is a comprehensive legal news portal which is committed to providing accurate'
        ' and honest news about legal developments.')
    no_stylesheets = True
    use_embedded_content = False
    encoding = 'utf-8'
    language = 'en_IN'
    remove_attributes = ['height', 'width', 'style'] 
    masthead_url = 'https://www.livelaw.in/images/logo.png'
    oldest_article = 1
    max_articles_per_feed = 40
    remove_empty_feeds = True
    ignore_duplicate_articles = {'title', 'url'}
    extra_css = """
    [data-datestring]{font-size:smaller;}
    p{text-align: justify; font-size: 100%}
    """ 
    keep_only_tags = [
        classes('trending_heading author-on-detail details-date-time detail_img_cover details-content-story')
    ]

    remove_tags = [
        classes('in-image-ad-wrap'),
        dict(name = 'div', attrs = {'id' : lambda x: x and x.startswith('inside_post_content_ad')}),    
        dict(name = 'div', attrs = {'id' : lambda x: x and x.startswith('filler_ad')})
    ]
    
    def articles_from_soup(self, soup):
        ans = []
        div = soup.find('div', **classes('news_listing_section_mixin'))
        for	h2 in div.findAll('h2', **classes('text_heading')):
            a = h2.find('a', href = True)
            title = self.tag_to_string(a)
            url = absurl(a['href'])
            d = h2.find_next_sibling('div')
            date = parse_date(self.tag_to_string(d).replace(' AM GMT', ':00 +0530').replace(' PM GMT', ':00 +0530'))
            today = (datetime.now(timezone.utc)).replace(microsecond=0)
            if (today - date) > timedelta(self.oldest_article):
                url = ''
        
            if not url or not title:
                    continue
                
            self.log('\t', title)
            self.log('\t\t', url)
            ans.append({'title': title,'url': url})
        return ans

    def parse_index(self):
        soup = self.index_to_soup('https://www.livelaw.in')
        nav_div = soup.find('div', **classes('navbar_center'))
        section_list = []

        # Finding all the section titles that are acceptable
        for a in nav_div.findAll(['a']):
            if self.is_accepted_entry(a):
                section_list.append((self.tag_to_string(a), absurl(a['href'])))
        feeds = []

        # For each section title, fetch the article urls
        for section in section_list:
            section_title = section[0]
            section_url = section[1]
            self.log(section_title, section_url)
            soup = self.index_to_soup(section_url)
            articles = self.articles_from_soup(soup)
            if articles:
                feeds.append((section_title, articles))
        return feeds
    
    def is_accepted_entry(self, entry):
        # Those sections in the top nav bar that we will omit
        omit_list = [
            'videos', 'job-updates', 'events-corner', 'sponsored', 'hindi.livelaw.in', 'javascript:void(0);',
        ]
        is_accepted = True
        for omit_entry in omit_list:
            if entry['href'].endswith(omit_entry):
                is_accepted = False
                break
        return is_accepted

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'