#!/usr/bin/env python
# vim:fileencoding=utf-8
import json
import re
from collections import defaultdict
from datetime import date

from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree

def absurl(url):
    if url.startswith('/'):
        url = 'https://www.thehindu.com' + url
    return url


class TheHindu(BasicNewsRecipe):
    title = 'The Hindu'
    __author__ = 'unkn0wn'
    description = 'Articles from The Hindu, Today\'s Paper.'
    language = 'en_IN'
    no_stylesheets = True
    masthead_url = 'https://www.thehindu.com/theme/images/th-online/thehindu-logo.svg'
    remove_attributes = ['style', 'height', 'width']

    extra_css = '''
        .caption {font-size:small; text-align:center;}
        .author, .dateLine {font-size:small;}
        .subhead, .subhead_lead, .bold {font-weight:bold;}
        img {display:block; margin:0 auto;}
        .italic, .sub-title {font-style:italic; color:#202020;}
    '''

    recipe_specific_options = {
        'location': {
            'short': 'The name of the local edition',
            'long': ('If The Hindu is available in your local town/city, '
                     'set this to your location, for example, hyderabad\n'
                     'Available Editions: bengaluru, chennai, coimbatore, delhi, '
                     'erode, hyderabad, international, kochi, kolkata,\n'
                     'kozhikode, madurai, mangalore, mumbai, thiruvananthapuram, '
                     'tiruchirapalli, vijayawada, visakhapatnam'),
            'default': 'international'
        },
        'date': {
            'short': 'The date of the edition to download (YYYY-MM-DD format)',
            'long': 'For example, 2023-01-28'
        }
    }

    ignore_duplicate_articles = {'url'}

    keep_only_tags = [
        classes('article-section')
    ]

    remove_tags = [
        classes('hide-mobile comments-shares share-page editiondetails')
    ]

    def preprocess_html(self, soup):
        for cap in soup.findAll('p', attrs={'class':'caption'}):
            cap.name = 'figcaption'
        for img in soup.findAll('img', attrs={'data-original':True}):
            img['src'] = img['data-original']
        for h3 in soup.findAll(**classes('sub-title')):
            h3.name = 'p'
        return soup

    def parse_index(self):
        local_edition = 'th_international'
        d = self.recipe_specific_options.get('location')
        if d and isinstance(d, str):
            local_edition = 'th_' + d

        past_edition = self.recipe_specific_options.get('date')

        dt = date.today()
        if past_edition and isinstance(past_edition, str):
            year, month, day = (int(x) for x in past_edition.split('-'))
            dt = date(year, month, day)

        today = dt.strftime('%Y-%m-%d')

        self.log('Downloading The Hindu, ' + local_edition[3:] + ' edition, ' + today)
        url = absurl('/todays-paper/' + today + '/' + local_edition + '/')

        mag_url = None
        if dt.weekday() == 0:
            mag_url = url + '?supplement=' + local_edition + '-epbs'
        if dt.weekday() == 4:
            mag_url = url + '?supplement=' + local_edition + '-fr'
        if dt.weekday() == 5:
            mag_url = url + '?supplement=' + local_edition + '-mp'
        if dt.weekday() == 6:
            mag_url = url + '?supplement=' + local_edition + '-sm'

        raw = self.index_to_soup(url, raw=True)
        soup = self.index_to_soup(raw)
        ans = self.hindu_parse_index(soup)
        cover = soup.find(attrs={'class':'hindu-ad'})
        if cover:
            self.cover_url = cover.img['src']
        if not ans:
            raise ValueError(
                    'The Hindu Newspaper is not published Today.'
                )
        if mag_url:
            self.log('\nFetching Magazine')
            soup = self.index_to_soup(mag_url)
            ans2 = self.hindu_parse_index(soup)
            if ans2:
                return ans + ans2
            self.log('\nMagazine not Found')
            return ans
        return ans

    def hindu_parse_index(self, soup):
        for script in soup.findAll('script'):
            if not self.tag_to_string(script).__contains__('grouped_articles = {"'):
                continue
            if script is not None:
                art = re.search(r'grouped_articles = ({\".*)', self.tag_to_string(script))
                data = json.JSONDecoder().raw_decode(art.group(1))[0]

                feeds_dict = defaultdict(list)

                a = json.dumps(data)
                for sec in json.loads(a):
                    for item in data[sec]:
                        section = sec.replace('TH_', '')
                        title = item['articleheadline']
                        url = absurl(item['href'])
                        desc = 'Page no.' + item['pageno'] + ' | ' + item['teaser_text'] or ''
                        self.log('            ', title, '\n\t', url)
                        feeds_dict[section].append({"title": title, "url": url, "description": desc})
                return [(section, articles) for section, articles in feeds_dict.items()]
            else:
                return []


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