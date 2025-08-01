#!/usr/bin/env python
# vim:fileencoding=utf-8
import json
import re
from collections import OrderedDict
from urllib.parse import urlencode, urljoin

from mechanize import Request

from calibre import browser, random_user_agent
from calibre.web.feeds.news import BasicNewsRecipe, classes


class HBR(BasicNewsRecipe):
    title = 'Harvard Business Review'
    __author__ = 'unkn0wn, updated by ping'
    description = (
        'Harvard Business Review is the leading destination for smart management thinking. '
        'Through its flagship magazine, books, and digital content and tools published on HBR.org, '
        'Harvard Business Review aims to provide professionals around the world with rigorous insights '
        'and best practices to help lead themselves and their organizations more effectively and to '
        'make a positive impact.'
    )
    language = 'en'
    masthead_url = 'https://hbr.org/resources/css/images/hbr_logo.svg'
    publication_type = 'magazine'
    encoding = 'utf-8'
    remove_javascript = True
    no_stylesheets = True
    auto_cleanup = False
    compress_news_images = True
    ignore_duplicate_articles = {'url'}
    base_url = 'https://hbr.org'

    remove_attributes = ['height', 'width', 'style']
    extra_css = '''
        h1.article-hed { font-size: x-large; margin-bottom: 0.4rem; }
        .article-dek {  font-size: large; font-style: italic; margin-bottom: 1rem; }
        .article-byline { margin-top: 0.7rem; font-size: medium; font-style: normal; font-weight: bold; }
        .pub-date { font-size: small; margin-bottom: 1rem; }
        img {
            display: block; margin-bottom: 0.3rem; max-width: 100%; height: auto;
            box-sizing: border-box;
        }
        .container--caption-credits-hero, .container--caption-credits-inline, span.credit { font-size: small; }
        .question { font-weight: bold; }
        .description-text {
            margin: 1rem 0;
            border-top: 1px solid gray;
            padding-top: 0.5rem;
            font-style: italic;
        }
        '''

    keep_only_tags = [
        classes(
            'headline-container article-dek-group pub-date hero-image-content '
            'article-body standard-content content'
        ),
        dict(name=['article'], class_=['hbr-article-body']),
        dict(name=['div'], class_=['article-content']),
        dict(name=['main']),
    ]

    remove_tags = [
        classes(
            'left-rail--container translate-message follow-topic '
            'newsletter-container by-prefix related-topics--common '
            'related-content subscription-banner paywall'
        ),
        dict(name=['article-sidebar', 'aside']),
        dict(name=['div'], class_=['paywall', 'subscription-required']),
    ]

    def preprocess_raw_html(self, raw_html, article_url):
        soup = self.soup(raw_html)

        # break author byline out of list
        byline_list = soup.find('ul', class_='article-byline-list')
        if byline_list:
            byline = byline_list.parent
            byline.append(
                ', '.join(
                    [
                        self.tag_to_string(author)
                        for author in byline_list.find_all(class_='article-author')
                    ]
                )
            )
            byline_list.decompose()

        # Try to extract full article content via API
        content_ele = soup.find(
            'content',
            attrs={
                'data-index': True,
                'data-page-year': True,
                'data-page-month': True,
                'data-page-seo-title': True,
                'data-page-slug': True,
            },
        )
        
        if content_ele:
            try:
                endpoint_url = 'https://hbr.org/api/article/piano/content?' + urlencode(
                    {
                        'year': content_ele['data-page-year'],
                        'month': content_ele['data-page-month'],
                        'seotitle': content_ele['data-page-seo-title'],
                    }
                )
                data = {
                    'contentKey': content_ele['data-index'],
                    'pageSlug': content_ele['data-page-slug'],
                }
                headers = {
                    'User-Agent': random_user_agent(),
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                    'Content-Type': 'application/json',
                    'Referer': article_url,
                }
                br = browser()
                req = Request(
                    endpoint_url,
                    headers=headers,
                    data=json.dumps(data),
                    method='POST',
                    timeout=self.timeout,
                )
                res = br.open(req)
                article = json.loads(res.read())
                new_soup = self.soup(article['content'])
                # clear out existing partial content
                for c in list(content_ele.children):
                    c.extract()  # use extract() instead of decompose() because of strings
                content_ele.append(new_soup.body)
                self.log('Successfully fetched full article content via API')
            except Exception as e:
                self.log('Failed to fetch full article content via API:', str(e))
                self.log('Falling back to existing content')
        else:
            self.log('Content element with required data attributes not found, using existing content')
        
        return str(soup)

    def get_browser(self):
        br = BasicNewsRecipe.get_browser(self)
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        return br

    recipe_specific_options = {
        'issue': {
            'short': 'Enter the Issue Number you want to download ',
            'long': 'For example, 2403'
        }
    }

    def parse_index(self):
        d = self.recipe_specific_options.get('issue')
        if not (d and isinstance(d, str)):
            soup = self.index_to_soup(f'{self.base_url}/magazine')
            a = soup.find('a', href=lambda x: x and x.startswith('/archive-toc/'))
            cov_url = a.find('img', attrs={'src': True})['src']
            self.cover_url = urljoin(self.base_url, cov_url)
            issue_url = urljoin(self.base_url, a['href'])
        else:
            issue_url = 'https://hbr.org/archive-toc/BR' + d
            mobj = re.search(r'archive-toc/(?P<issue>(BR)?\d+)\b', issue_url)
            if mobj:
                self.cover_url = f'https://hbr.org/resources/images/covers/{mobj.group("issue")}_500.png'

        self.log('Downloading issue:', issue_url)
        soup = self.index_to_soup(issue_url)
        issue_title = soup.find('h1')
        if issue_title:
            self.timefmt = f' [{self.tag_to_string(issue_title)}]'

        feeds = OrderedDict()
        for h3 in soup.find_all('h3', attrs={'class': 'hed'}):
            article_link_ele = h3.find('a')
            if not article_link_ele:
                continue

            article_ele = h3.find_next_sibling(
                'div', attrs={'class': 'stream-item-info'}
            )
            if not article_ele:
                continue

            title = self.tag_to_string(article_link_ele)
            url = urljoin(self.base_url, article_link_ele['href'])

            authors_ele = article_ele.select('ul.byline li')
            authors = ', '.join([self.tag_to_string(a) for a in authors_ele])

            article_desc = ''
            dek_ele = h3.find_next_sibling('div', attrs={'class': 'dek'})
            if dek_ele:
                article_desc = self.tag_to_string(dek_ele) + ' | ' + authors
            section_ele = (
                h3.findParent('li')
                .find_previous_sibling('div', **classes('stream-section-label'))
                .find('h4')
            )
            section_title = self.tag_to_string(section_ele).title()
            feeds.setdefault(section_title, []).append(
                {'title': title, 'url': url, 'description': article_desc}
            )
        return feeds.items()