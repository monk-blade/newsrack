#!/usr/bin/env python
import json
import re

from calibre.web.feeds.news import BasicNewsRecipe


class IndiaToday(BasicNewsRecipe):
    title = u'India Today Magazine'
    language = 'en_IN'
    __author__ = 'unkn0wn'
    no_stylesheets = True
    use_embedded_content = False
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    description = (
        'India’s Most Reputed, Credible and Popular news magazine.'
        ' Read the most preferred magazine of 9.5 million Indians to access highly researched and unbiased content.'
    )
    masthead_url = 'https://akm-img-a-in.tosshub.com/sites/all/themes/itg/logo.png'

    extra_css = '''
        #sub-h {font-style:italic; color:#202020;}
        .body_caption, #imgcap, .mos__alt .caption, .caption-drupal-entity, .calibre-nuked-tag-figcaption {font-size:small; text-align:center;}
        #author, .authors__container {font-size:small;}
        blockquote {color:#404040;}
    '''

    remove_tags = [dict(attrs={id:['tab-link-wrapper-plugin']})]

    recipe_specific_options = {
        'date': {
            'short': 'The date of the edition to download (DD-MM-YYYY format)',
            'long': 'For example, 22-07-2024'
        }
    }

    def get_cover_url(self):
        d = self.recipe_specific_options.get('date')
        if not (d and isinstance(d, str)):
            soup = self.index_to_soup(
                'https://www.readwhere.com/magazine/the-india-today-group/India-Today/1154'
            )
            for citem in soup.findAll(
                'meta', content=lambda s: s and s.endswith('/magazine/300/new')
            ):
                return citem['content'].replace('300', '600')

    def parse_index(self):
        issue = 'https://www.indiatoday.in/magazine'
        d = self.recipe_specific_options.get('date')
        if d and isinstance(d, str):
            issue = issue + '/' + d
        soup = self.index_to_soup(issue)

        section = None
        sections = {}

        for tag in soup.findAll('div', attrs={'class': lambda x: x and 'NoCard_story__grid__' in x}):
            sec = tag.find('div', attrs={'class': lambda x: x and 'NoCard_header__nav__' in x})
            section = self.tag_to_string(sec).strip()
            self.log(section)
            sections[section] = []

            for art in tag.findAll('article'):
                title = self.tag_to_string(art.find(attrs={'class':lambda x: x and 'NoCard_articletitle__' in x})).strip()
                url = art.find('a', href=True, title=True)['href']
                if url.startswith('/'):
                    url = 'https://www.indiatoday.in' + url
                desc = self.tag_to_string(art.find(attrs={'class':lambda x: x and 'NoCard_story__shortcont__' in x})).strip()
                self.log('\t', title, '\n\t', desc, '\n\t\t', url)
                sections[section].append({'title': title, 'url': url, 'description': desc})

        def sort_key(x):
            section = x[0]
            try:
                return (
                    "Editor's Note", 'Cover Story', 'The Big Story', 'Upfront',
                    'NATION', 'INTERVIEW'
                ).index(section)
            except Exception:
                return 99999999

        return sorted(sections.items(), key=sort_key)

    def preprocess_html(self, soup):
        for quo in soup.findAll(attrs={'class':'quotes'}):
            quo.name = 'blockquote'
        return soup

    def preprocess_raw_html(self, raw, *a):
        m = re.search(r'id="__NEXT_DATA__" type="application/json">', raw)
        raw = raw[m.start():]
        raw = raw.split('>', 1)[1]
        data = json.JSONDecoder().raw_decode(raw)[0]
        data = data['props']['pageProps']['initialState']['server']['page_data']
        title = data['title']
        body = '<div>' + data['description'] + '</div>'

        slug = desc = image = author = date = imagecap = city = ''

        if 'slug' in data:
            slug = '<div>' + data['slug'] + '</div>\n'
        if 'description_short' in data:
            desc = '<p id="sub-h">' + data['description_short'] + '</p>\n'
        if data.get('author'):
            author = ', '.join([names['title'] for names in data['author']])
        if 'city' in data:
            city = data['city']
        if 'datetime_updated' in data:
            date = data['datetime_updated']
        if 'image_main' in data:
            image = '<br/><img src="{}">'.format(data['image_main'])
            if 'image_caption' in data:
                imagecap = '<div id="imgcap">' + data['image_caption'] + '</div>'

        return ('<html><body>' + slug + '<h1>' + title + '</h1>\n' + desc + '<div id="author">'
                + author + '<span> ' + city + ' UPDATED: ' + date + '</span></div>\n' + image + imagecap + body +
                '</body></html>')