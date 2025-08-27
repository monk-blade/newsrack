import os, sys
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime

_name = 'Outlook Magazine'

class outlook(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = 'unkn0wn'
    description = (
        'Outlook covers the latest India news, analysis, business news and long-form stories on culture,'
        " money market and personal finance. Read India's best online magazine."
    )
    language = 'en_IN'
    use_embedded_content = False
    no_stylesheets = True
    remove_javascript = True
    remove_attributes = ['height', 'width', 'style']
    ignore_duplicate_articles = {'url'}
    resolve_internal_links = True
    simultaneous_downloads = 9
    masthead_url = 'https://images.assettype.com/outlookindia/2024-02/96fb06ce-1cc8-410e-ad6c-da4de57405f8/Outlook.svg'
    extra_css = '''
        .subcap-story {font-style:italic; color:#202020;}
        .story-slug, .article-name-date {font-size:small; color:#404040;}
        .main-img-div, .sb-image {font-size:small; text-align:center;}
        em { color:#202020; }
    '''
    # Remove browser_type = 'webengine' for CI compatibility

    keep_only_tags = [
        classes('story-slug story-title subcap-story article-name-date w-93')
    ]

    remove_tags = [
        dict(name='svg'),
        dict(
            name='a',
            attrs={'href': lambda x: x and x.startswith('https://www.whatsapp.com/')},
        ),
        classes(
            'ads-box ad-slot olm-story-related-stories hd-summry info-img-absolute mobile-info-id story-dec-time-mobile sb-also-read ads-box1 story-mag-issue-section'
        ),
    ]

    recipe_specific_options = {
        'date': {
            'short': 'The date of the edition to download (DD-Month-YYYY format)',
            'long': 'For example, 10-june-2024',
        }
    }

    def parse_index(self):
        self.log(
            'try again and again\n***\nif this recipe fails, report it on: '
            'https://www.mobileread.com/forums/forumdisplay.php?f=228\n***\n'
        )

        d = self.recipe_specific_options.get('date')
        if d and isinstance(d, str):
            url = 'https://www.outlookindia.com/magazine/' + d
        else:
            soup = self.index_to_soup('https://www.outlookindia.com/magazine')
            a = soup.find('a', attrs={'aria-label': 'magazine-cover-image'})
            if not a:
                # Fallback: try to find any magazine link
                a = soup.find('a', href=lambda x: x and '/magazine/' in x)
            if not a:
                self.abort_recipe_processing('Could not find magazine cover link')
            url = a['href']

        self.log('Downloading issue:', url)

        soup = self.index_to_soup(url)
        
        # Extract issue name from page title
        page_title = soup.find('title')
        if page_title:
            title_text = self.tag_to_string(page_title)
            self.log(f'Page title: {title_text}')
            
            # Look for "Outlook Magazine Issue - " pattern
            if '|' in title_text and 'Outlook Magazine Issue -' in title_text:
                # Split by | and find the part with "Outlook Magazine Issue -"
                parts = title_text.split('|')
                for part in parts:
                    part = part.strip()
                    if 'Outlook Magazine Issue -' in part:
                        self.title = part
                        self.log(f'Set recipe title to: {self.title}')
                        break

        cov = soup.find(attrs={'aria-label': 'magazine-cover-image'})
        if cov and cov.img:
            self.cover_url = cov.img['src'].split('?')[0]
        
        summ = soup.find(attrs={'data-test-id': 'magazine-summary'})
        if summ:
            self.description = self.tag_to_string(summ)
        
        tme = soup.find(attrs={'class': 'arr__timeago'})
        if tme:
            self.timefmt = ' [' + self.tag_to_string(tme).split('-')[-1].strip() + ']'

        ans = []

        for div in soup.findAll(attrs={'class': 'article-heading-two'}):
            a = div.a
            if not a:
                continue
            url = a['href']
            title = self.tag_to_string(a)
            desc = ''
            p = div.find_next_sibling(
                'p', attrs={'class': lambda x: x and 'article-desc' in x.split()}
            )
            if p:
                desc = self.tag_to_string(p)
            auth = div.find_next_sibling('p', attrs={'class': 'author'})
            if auth:
                desc = self.tag_to_string(auth) + ' | ' + desc
            self.log('\t', title)
            self.log('\t', desc)
            self.log('\t\t', url)
            ans.append({'title': title, 'url': url, 'description': desc})
        return [('Articles', ans)]

    def preprocess_html(self, soup):
        if sub := soup.find(**classes('subcap-story')):
            sub.name = 'p'
        for h2 in soup.findAll(['h2', 'h3']):
            h2.name = 'h4'
        for img in soup.findAll('img', attrs={'data-src': True}):
            img['src'] = img['data-src'].split('?')[0] + '?w=600'
        return soup