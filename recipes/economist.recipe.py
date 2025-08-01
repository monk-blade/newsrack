#!/usr/bin/env  python
# License: GPLv3 Copyright: 2008, Kovid Goyal <kovid at kovidgoyal.net>

import json
import re
import time
from collections import defaultdict
from datetime import datetime, timedelta
from urllib.parse import quote, urlencode
from uuid import uuid4

from html5_parser import parse
from lxml import etree

from calibre import replace_entities
from calibre.ebooks.BeautifulSoup import BeautifulSoup, NavigableString, Tag
from calibre.ptempfile import PersistentTemporaryFile
from calibre.scraper.simple import read_url
from calibre.utils.date import parse_only_date
from calibre.web.feeds.news import BasicNewsRecipe


def E(parent, name, text='', **attrs):
    ans = parent.makeelement(name, **attrs)
    ans.text = text
    parent.append(ans)
    return ans


def process_node(node, html_parent):
    ntype = node.get('type')
    if ntype == 'tag':
        c = html_parent.makeelement(node['name'])
        c.attrib.update({k: v or '' for k, v in node.get('attribs', {}).items()})
        html_parent.append(c)
        for nc in node.get('children', ()):
            process_node(nc, c)
    elif ntype == 'text':
        text = node.get('data')
        if text:
            text = replace_entities(text)
            if len(html_parent):
                t = html_parent[-1]
                t.tail = (t.tail or '') + text
            else:
                html_parent.text = (html_parent.text or '') + text


def safe_dict(data, *names):
    ans = data
    for x in names:
        ans = ans.get(x) or {}
    return ans


class JSONHasNoContent(ValueError):
    pass


def load_article_from_json(raw, root):
    # open('/t/raw.json', 'w').write(raw)
    data = json.loads(raw)
    body = root.xpath('//body')[0]
    article = E(body, 'article')
    E(article, 'div', data['flyTitle'], style='color: red; font-size:small; font-weight:bold;')
    E(article, 'h1', data['title'], title=safe_dict(data, 'url', 'canonical') or '')
    E(article, 'div', data['rubric'], style='font-style: italic; color:#202020;')
    try:
        date = data['dateModified']
    except Exception:
        date = data['datePublished']
    dt = datetime.fromisoformat(date[:-1]) + timedelta(seconds=time.timezone)
    dt = dt.strftime('%b %d, %Y %I:%M %p')
    if data['dateline'] is None:
        E(article, 'p', dt, style='color: gray; font-size:small;')
    else:
        E(article, 'p', dt + ' | ' + (data['dateline']), style='color: gray; font-size:small;')
    main_image_url = safe_dict(data, 'image', 'main', 'url').get('canonical')
    if main_image_url:
        div = E(article, 'div')
        try:
            E(div, 'img', src=main_image_url)
        except Exception:
            pass
    for node in data.get('text') or ():
        process_node(node, article)


def process_web_list(li_node):
    li_html = ''
    for li in li_node['items']:
        if li.get('textHtml'):
            li_html += f'<li>{li.get("textHtml")}</li>'
        else:
            li_html +=  f'<li>{li.get("text", "")}</li>'
    return li_html


def process_info_box(bx):
    info = ''
    for x in safe_dict(bx, 'components'):
        info += f'<blockquote>{process_web_node(x)}</blockquote>'
    return info


def process_web_node(node):
    ntype = node.get('type', '')
    if ntype == 'CROSSHEAD':
        if node.get('textHtml'):
            return f'<h4>{node.get("textHtml")}</h4>'
        return f'<h4>{node.get("text", "")}</h4>'
    elif ntype in ['PARAGRAPH', 'BOOK_INFO']:
        if node.get('textHtml'):
            return f'<p>{node.get("textHtml")}</p>'
        return f'<p>{node.get("text", "")}</p>'
    elif ntype == 'IMAGE':
        alt = '' if node.get('altText') is None else node.get('altText')
        cap = ''
        if node.get('caption'):
            if node['caption'].get('textHtml') is not None:
                cap = node['caption']['textHtml']
        return f'<div><img src="{node["url"]}" title="{alt}"></div><div style="text-align:center; font-size:small;">{cap}</div>'
    elif ntype == 'PULL_QUOTE':
        if node.get('textHtml'):
            return f'<blockquote>{node.get("textHtml")}</blockquote>'
        return f'<blockquote>{node.get("text", "")}</blockquote>'
    elif ntype == 'DIVIDER':
        return '<hr>'
    elif ntype == 'INFOGRAPHIC':
        if node.get('fallback'):
            return process_web_node(node['fallback'])
    elif ntype == 'INFOBOX':
        return process_info_box(node)
    elif ntype == 'UNORDERED_LIST':
        if node.get('items'):
            return process_web_list(node)
    elif ntype:
        print('** ', ntype)
    return ''


def load_article_from_web_json(raw):
    # open('/t/raw.json', 'w').write(raw)
    body = ''
    try:
        data = json.loads(raw)['props']['pageProps']['cp2Content']
    except Exception:
        data = json.loads(raw)['props']['pageProps']['content']
    body += f'<div style="color: red; font-size:small; font-weight:bold;">{data.get("flyTitle", "")}</div>'
    body += f'<h1>{data["headline"]}</h1>'
    if data.get('rubric') and data.get('rubric') is not None:
        body += f'<div style="font-style: italic; color:#202020;">{data.get("rubric", "")}</div>'
    try:
        date = data['dateModified']
    except Exception:
        date = data['datePublished']
    dt = datetime.fromisoformat(date[:-1]) + timedelta(seconds=time.timezone)
    dt = dt.strftime('%b %d, %Y %I:%M %p')
    if data.get('dateline') is None:
        body += f'<p style="color: gray; font-size: small;">{dt}</p>'
    else:
        body += f'<p style="color: gray; font-size: small;">{dt + " | " + (data["dateline"])}</p>'
    main_image_url = safe_dict(data, 'leadComponent') or ''
    if main_image_url:
        body += process_web_node(data['leadComponent'])
    for node in data.get('body'):
        body += process_web_node(node)
    return '<html><body><article>' + body + '</article></body></html>'


def cleanup_html_article(root):
    main = root.xpath('//main')[0]
    body = root.xpath('//body')[0]
    for child in tuple(body):
        body.remove(child)
    body.append(main)
    main.set('id', '')
    main.tag = 'article'
    for x in root.xpath('//*[@style]'):
        x.set('style', '')
    for x in root.xpath('//button'):
        x.getparent().remove(x)


def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


def new_tag(soup, name, attrs=()):
    impl = getattr(soup, 'new_tag', None)
    if impl is not None:
        return impl(name, attrs=dict(attrs))
    return Tag(soup, name, attrs=attrs or None)


class NoArticles(Exception):
    pass


def process_url(url):
    if url.startswith('/'):
        url = 'https://www.economist.com' + url
    return url


class Economist(BasicNewsRecipe):
    title = 'The Economist'
    language = 'en_GB'
    encoding = 'utf-8'
    masthead_url = 'https://www.livemint.com/lm-img/dev/economist-logo-oneline.png'

    __author__ = 'Kovid Goyal'
    description = (
        'Global news and current affairs from a European'
        ' perspective. Best downloaded on Friday mornings (GMT)'
    )
    extra_css = '''
        em { color:#202020; }
        img {display:block; margin:0 auto;}
    '''
    oldest_article = 7.0
    resolve_internal_links = True
    remove_tags = [
        dict(name=['script', 'noscript', 'title', 'iframe', 'cf_floatingcontent', 'aside', 'footer', 'svg']),
        dict(attrs={'aria-label': 'Article Teaser'}),
        dict(attrs={'id': 'player'}),
        dict(attrs={
                'class': [
                    'dblClkTrk', 'ec-article-info', 'share_inline_header',
                    'related-items', 'main-content-container', 'ec-topic-widget',
                    'teaser', 'blog-post__bottom-panel-bottom', 'blog-post__comments-label',
                    'blog-post__foot-note', 'blog-post__sharebar', 'blog-post__bottom-panel',
                    'newsletter-form', 'share-links-header', 'teaser--wrapped', 'latest-updates-panel__container',
                    'latest-updates-panel__article-link', 'blog-post__section'
                ]
            }
        ),
        dict(attrs={
                'class': lambda x: x and 'blog-post__siblings-list-aside' in x.split()}),
        dict(attrs={'id': lambda x: x and 'gpt-ad-slot' in x}),
        classes(
            'share-links-header teaser--wrapped latest-updates-panel__container'
            ' latest-updates-panel__article-link blog-post__section newsletter-form blog-post__bottom-panel'
        )
    ]
    keep_only_tags = [dict(name='article', id=lambda x: not x)]
    no_stylesheets = True
    remove_attributes = ['data-reactid', 'width', 'height']
    # economist.com has started throttling after about 60% of the total has
    # downloaded with connection reset by peer (104) errors.
    delay = 3
    browser_type = 'webengine'
    from_archive = True
    recipe_specific_options = {
        'date': {
            'short': 'The date of the edition to download (YYYY-MM-DD format)',
            'long': 'For example, 2024-07-19',
        },
        'res': {
            'short': 'For hi-res images, select a resolution from the\nfollowing options: 834, 960, 1096, 1280, 1424',
            'long': 'This is useful for non e-ink devices, and for a lower file size\nthan the default, use from 480, 384, 360, 256.',
            'default': '600',
        },
        'de': {
            'short': 'Web Edition',
            'long': 'Yes/No. Digital Edition does not skip some articles based on your location.',
            'default': 'No',
        }
    }

    def __init__(self, *args, **kwargs):
        BasicNewsRecipe.__init__(self, *args, **kwargs)
        d = self.recipe_specific_options.get('de')
        if d and isinstance(d, str):
            if d.lower().strip() == 'yes':
                self.from_archive = True

    needs_subscription = False

    def get_browser(self, *args, **kwargs):
        if self.from_archive:
            kwargs['user_agent'] = (
                'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36 Liskov'
            )
            br = BasicNewsRecipe.get_browser(self, *args, **kwargs)
        else:
            kwargs['user_agent'] = 'TheEconomist-Lamarr-android'
            br = BasicNewsRecipe.get_browser(self, *args, **kwargs)
            br.addheaders += [
                ('accept', '*/*'),
                ('content-type', 'application/json'),
                ('apollographql-client-name', 'mobile-app-apollo'),
                ('apollographql-client-version', '3.50.0'),
                ('x-request-id', str(uuid4())),
            ]
        return br

    def publication_date(self):
        edition_date = self.recipe_specific_options.get('date')
        if edition_date and isinstance(edition_date, str):
            return parse_only_date(edition_date, as_utc=False)
        try:
            url = self.browser.open('https://www.economist.com/printedition').geturl()
        except Exception as e:
            self.log('Failed to fetch publication date with error: ' + str(e))
            return super().publication_date()
        return parse_only_date(url.split('/')[-1], as_utc=False)

    def economist_test_article(self):
        return [('Articles', [{'title':'test',
            'url':'https://www.economist.com/leaders/2025/03/13/americas-bullied-allies-need-to-toughen-up'
        }])]

    def economist_return_index(self, ans):
        if not ans:
            raise NoArticles(
                'Could not find any articles, either the '
                'economist.com server is having trouble and you should '
                'try later or the website format has changed and the '
                'recipe needs to be updated.'
            )
        return ans

    def get_content_id(self, ed_date):
        id_query = {
            'query': 'query EditionsQuery($from:Int$size:Int$ref:String!){section:canonical(ref:$ref){...EditionFragment __typename}}fragment EditionFragment on Content{hasPart(from:$from size:$size sort:"datePublished:desc"){total parts{id datePublished image{...ImageCoverFragment __typename}__typename}__typename}__typename}fragment ImageCoverFragment on Media{cover{headline width height url{canonical __typename}regionsAllowed __typename}__typename}',  # noqa: E501
            'operationName': 'EditionsQuery',
            'variables':'{"from":0,"size":24,"ref":"/content/d06tg8j85rifiq3oo544c6b9j61dno2n"}',
        }
        id_url = 'https://cp2-graphql-gateway.p.aws.economist.com/graphql?' + urlencode(id_query, safe='()!', quote_via=quote)
        raw_id_data = self.index_to_soup(id_url, raw=True)
        data = json.loads(raw_id_data)['data']['section']['hasPart']['parts']
        for x in data:
            if ed_date in x['datePublished']:
                return x['id']
        return None

    def parse_index(self):
        if self.from_archive:
            return self.parse_web_index()
        edition_date = self.recipe_specific_options.get('date')
        # return self.economist_test_article()
        # url = 'https://www.economist.com/weeklyedition/archive'
        query = {
            'query': 'query LatestWeeklyAutoEditionQuery($ref:String!){canonical(ref:$ref){hasPart(from:0 size:1 sort:"datePublished:desc"){parts{...WeeklyEditionFragment __typename}__typename}__typename}}fragment WeeklyEditionFragment on Content{id type datePublished image{...ImageCoverFragment __typename}url{canonical __typename}hasPart(size:100 sort:"publication.context.position"){parts{...ArticleFragment __typename}__typename}__typename}fragment ArticleFragment on Content{ad{grapeshot{channels{name __typename}__typename}__typename}articleSection{internal{id title:headline __typename}__typename}audio{main{id duration(format:"seconds")source:channel{id __typename}url{canonical __typename}__typename}__typename}byline dateline dateModified datePublished dateRevised flyTitle:subheadline id image{...ImageInlineFragment ...ImageMainFragment ...ImagePromoFragment __typename}print{title:headline flyTitle:subheadline rubric:description section{id title:headline __typename}__typename}publication{id tegID title:headline flyTitle:subheadline datePublished regionsAllowed url{canonical __typename}__typename}rubric:description source:channel{id __typename}tegID text(format:"json")title:headline type url{canonical __typename}topic contentIdentity{forceAppWebview mediaType articleType __typename}__typename}fragment ImageInlineFragment on Media{inline{url{canonical __typename}width height __typename}__typename}fragment ImageMainFragment on Media{main{url{canonical __typename}width height __typename}__typename}fragment ImagePromoFragment on Media{promo{url{canonical __typename}id width height __typename}__typename}fragment ImageCoverFragment on Media{cover{headline width height url{canonical __typename}regionsAllowed __typename}__typename}',  # noqa: E501
            'operationName': 'LatestWeeklyAutoEditionQuery',
            'variables': '{"ref":"/content/d06tg8j85rifiq3oo544c6b9j61dno2n"}',
        }
        if edition_date and isinstance(edition_date, str):
            content_id = self.get_content_id(edition_date)
            if content_id:
                query = {
                    'query': 'query SpecificWeeklyEditionQuery($path:String!){section:canonical(ref:$path){...WeeklyEditionFragment __typename}}fragment WeeklyEditionFragment on Content{id type datePublished image{...ImageCoverFragment __typename}url{canonical __typename}hasPart(size:100 sort:"publication.context.position"){parts{...ArticleFragment __typename}__typename}__typename}fragment ArticleFragment on Content{ad{grapeshot{channels{name __typename}__typename}__typename}articleSection{internal{id title:headline __typename}__typename}audio{main{id duration(format:"seconds")source:channel{id __typename}url{canonical __typename}__typename}__typename}byline dateline dateModified datePublished dateRevised flyTitle:subheadline id image{...ImageInlineFragment ...ImageMainFragment ...ImagePromoFragment __typename}print{title:headline flyTitle:subheadline rubric:description section{id title:headline __typename}__typename}publication{id tegID title:headline flyTitle:subheadline datePublished regionsAllowed url{canonical __typename}__typename}rubric:description source:channel{id __typename}tegID text(format:"json")title:headline type url{canonical __typename}topic contentIdentity{forceAppWebview mediaType articleType __typename}__typename}fragment ImageInlineFragment on Media{inline{url{canonical __typename}width height __typename}__typename}fragment ImageMainFragment on Media{main{url{canonical __typename}width height __typename}__typename}fragment ImagePromoFragment on Media{promo{url{canonical __typename}id width height __typename}__typename}fragment ImageCoverFragment on Media{cover{headline width height url{canonical __typename}regionsAllowed __typename}__typename}',  # noqa: E501
                    'operationName': 'SpecificWeeklyEditionQuery',
                    'variables': '{{"path":"{}"}}'.format(content_id),
                }
        url = 'https://cp2-graphql-gateway.p.aws.economist.com/graphql?' + urlencode(query, safe='()!', quote_via=quote)
        try:
            if edition_date and isinstance(edition_date, str):
                if not content_id:
                    self.log(edition_date, ' not found, trying web edition.')
                    self.from_archive = True
                    return self.parse_web_index()
            raw = self.index_to_soup(url, raw=True)
        except Exception:
            self.log('Digital Edition Server is not reachable, try again after some time.')
            self.from_archive = True
            return self.parse_web_index()
        ans = self.economist_parse_index(raw)
        return self.economist_return_index(ans)

    def economist_parse_index(self, raw):
        # edition_date = self.recipe_specific_options.get('date')
        # if edition_date and isinstance(edition_date, str):
        #     data = json.loads(raw)['data']['section']
        # else:
        #     data = json.loads(raw)['data']['canonical']['hasPart']['parts'][0]
        try:
            data = json.loads(raw)['data']['section']
        except KeyError:
            data = json.loads(raw)['data']['canonical']['hasPart']['parts'][0]
        dt = datetime.fromisoformat(data['datePublished'][:-1]) + timedelta(seconds=time.timezone)
        dt = dt.strftime('%b %d, %Y')
        self.timefmt = ' [' + dt + ']'
        # get local issue cover, title
        try:
            region = json.loads(self.index_to_soup('https://geolocation-db.com/json', raw=True))['country_code']
        except Exception:
            region = ''
        for cov in data['image']['cover']:
            if region in cov['regionsAllowed']:
                self.description = cov['headline']
                self.cover_url = cov['url']['canonical'].replace('economist.com/',
                    'economist.com/cdn-cgi/image/width=960,quality=80,format=auto/')
                break
        else:
            self.description = data['image']['cover'][0]['headline']
            self.cover_url = data['image']['cover'][0]['url']['canonical'].replace('economist.com/',
            'economist.com/cdn-cgi/image/width=960,quality=80,format=auto/')
        self.log('Got cover:', self.cover_url, '\n', self.description)

        feeds_dict = defaultdict(list)
        for part in safe_dict(data, 'hasPart', 'parts'):
            try:
                section = part['articleSection']['internal'][0]['title']
            except Exception:
                section = safe_dict(part, 'print', 'section', 'title') or 'section'
            if section not in feeds_dict:
                self.log(section)
            title = safe_dict(part, 'title')
            desc = safe_dict(part, 'rubric') or ''
            sub = safe_dict(part, 'flyTitle') or ''
            if sub and section != sub:
                desc = sub + ' :: ' + desc
            pt = PersistentTemporaryFile('.html')
            pt.write(json.dumps(part).encode('utf-8'))
            pt.close()
            url = 'file:///' + pt.name
            feeds_dict[section].append({'title': title, 'url': url, 'description': desc})
            self.log('\t', title, '\n\t\t', desc)
        return list(feeds_dict.items())

    def populate_article_metadata(self, article, soup, first):
        if not self.from_archive:
            article.url = soup.find('h1')['title']

    def preprocess_html(self, soup):
        width = '600'
        w = self.recipe_specific_options.get('res')
        if w and isinstance(w, str):
            width = w
        for img in soup.findAll('img', src=True):
            qua = 'economist.com/cdn-cgi/image/width=' + width + ',quality=80,format=auto/'
            img['src'] = img['src'].replace('economist.com/', qua)
        return soup

    def preprocess_raw_html(self, raw, url):
        if self.from_archive:
            return self.preprocess_raw_web_html(raw, url)

        # open('/t/raw.html', 'wb').write(raw.encode('utf-8'))

        body = '<html><body><article></article></body></html>'
        root = parse(body)
        load_article_from_json(raw, root)

        if '/interactive/' in url:
            return ('<html><body><article><h1>' + root.xpath('//h1')[0].text + '</h1><em>'
                    'This article is supposed to be read in a browser.'
                    '</em></article></body></html>')

        for div in root.xpath('//div[@class="lazy-image"]'):
            noscript = list(div.iter('noscript'))
            if noscript and noscript[0].text:
                img = list(parse(noscript[0].text).iter('img'))
                if img:
                    p = noscript[0].getparent()
                    idx = p.index(noscript[0])
                    p.insert(idx, p.makeelement('img', src=img[0].get('src')))
                    p.remove(noscript[0])
        for x in root.xpath('//*[name()="script" or name()="style" or name()="source" or name()="meta"]'):
            x.getparent().remove(x)
        # the economist uses <small> for small caps with a custom font
        for init in root.xpath('//span[@data-caps="initial"]'):
            init.set('style', 'font-weight:bold;')
        for x in root.xpath('//small'):
            if x.text and len(x) == 0:
                x.text = x.text.upper()
                x.tag = 'span'
                x.set('style', 'font-variant: small-caps')
        for h2 in root.xpath('//h2'):
            h2.tag = 'h4'
        for x in root.xpath('//figcaption'):
            x.set('style', 'text-align:center; font-size:small;')
        for x in root.xpath('//cite'):
            x.tag = 'blockquote'
            x.set('style', 'color:#404040;')
        raw = etree.tostring(root, encoding='unicode')
        return raw

    def parse_index_from_printedition(self):
        # return self.economist_test_article()
        edition_date = self.recipe_specific_options.get('date')
        if edition_date and isinstance(edition_date, str):
            url = 'https://www.economist.com/weeklyedition/' + edition_date
            self.timefmt = ' [' + edition_date + ']'
        else:
            url = 'https://www.economist.com/printedition'
        # raw = open('/t/raw.html').read()
        raw = self.index_to_soup(url, raw=True)
        # with open('/t/raw.html', 'wb') as f:
        #     f.write(raw)
        soup = self.index_to_soup(raw)
        # nav = soup.find(attrs={'class':'navigation__wrapper'})
        # if nav is not None:
        #     a = nav.find('a', href=lambda x: x and '/printedition/' in x)
        #     if a is not None:
        #         self.log('Following nav link to current edition', a['href'])
        #         soup = self.index_to_soup(process_url(a['href']))
        ans = self.economist_parse_index(soup)
        if not ans:
            raise NoArticles(
                'Could not find any articles, either the '
                'economist.com server is having trouble and you should '
                'try later or the website format has changed and the '
                'recipe needs to be updated.'
            )
        return ans

    def eco_find_image_tables(self, soup):
        for x in soup.findAll('table', align=['right', 'center']):
            if len(x.findAll('font')) in (1, 2) and len(x.findAll('img')) == 1:
                yield x

    def postprocess_html(self, soup, first):
        for img in soup.findAll('img', srcset=True):
            del img['srcset']
        for table in list(self.eco_find_image_tables(soup)):
            caption = table.find('font')
            img = table.find('img')
            div = new_tag(soup, 'div')
            div['style'] = 'text-align:left;font-size:70%'
            ns = NavigableString(self.tag_to_string(caption))
            div.insert(0, ns)
            div.insert(1, new_tag(soup, 'br'))
            del img['width']
            del img['height']
            img.extract()
            div.insert(2, img)
            table.replaceWith(div)
        return soup

    def canonicalize_internal_url(self, url, is_link=True):
        if url.endswith('/print'):
            url = url.rpartition('/')[0]
        return BasicNewsRecipe.canonicalize_internal_url(self, url, is_link=is_link)

    # archive code
    def parse_web_index(self):
        edition_date = self.recipe_specific_options.get('date')
        # return self.economist_test_article()
        if edition_date and isinstance(edition_date, str):
            url = 'https://www.economist.com/weeklyedition/' + edition_date
            self.timefmt = ' [' + edition_date + ']'
        else:
            url = 'https://www.economist.com/weeklyedition'
        soup = self.index_to_soup(url)
        ans = self.economist_parse_web_index(soup)
        return self.economist_return_index(ans)

    def economist_parse_web_index(self, soup):
        script_tag = soup.find('script', id='__NEXT_DATA__')
        if script_tag is not None:
            data = json.loads(script_tag.string)
            # open('/t/raw.json', 'w').write(json.dumps(data, indent=2, sort_keys=True))
            self.description = safe_dict(data, 'props', 'pageProps', 'content', 'headline')
            self.timefmt = ' [' + safe_dict(data, 'props', 'pageProps', 'content', 'formattedIssueDate') + ']'
            self.cover_url = safe_dict(data, 'props', 'pageProps', 'content', 'cover', 'url').replace(
                'economist.com/', 'economist.com/cdn-cgi/image/width=960,quality=80,format=auto/').replace('SQ_', '')
            self.log('Got cover:', self.cover_url)

            feeds = []

            for part in safe_dict(
                data, 'props', 'pageProps', 'content', 'headerSections'
            ) + safe_dict(data, 'props', 'pageProps', 'content', 'sections'):
                section = safe_dict(part, 'name') or ''
                if not section:
                    continue
                self.log(section)

                articles = []

                for ar in part['articles']:
                    title = safe_dict(ar, 'headline') or ''
                    url = process_url(safe_dict(ar, 'url') or '')
                    if not title or not url:
                        continue
                    desc = safe_dict(ar, 'rubric') or ''
                    sub = safe_dict(ar, 'flyTitle') or ''
                    if sub and section != sub:
                        desc = sub + ' :: ' + desc
                    self.log('\t', title, '\n\t', desc, '\n\t\t', url)
                    articles.append({'title': title, 'url': url, 'description': desc})
                feeds.append((section, articles))
            return feeds
        else:
            return []

    def preprocess_raw_web_html(self, raw, url):
        # open('/t/raw.html', 'wb').write(raw.encode('utf-8'))
        root_ = parse(raw)
        if '/interactive/' in url:
            return ('<html><body><article><h1>' + root_.xpath('//h1')[0].text + '</h1><em>'
                    'This article is supposed to be read in a browser'
                    '</em></article></body></html>')

        script = root_.xpath('//script[@id="__NEXT_DATA__"]')

        html = load_article_from_web_json(script[0].text)

        root = parse(html)
        for div in root.xpath('//div[@class="lazy-image"]'):
            noscript = list(div.iter('noscript'))
            if noscript and noscript[0].text:
                img = list(parse(noscript[0].text).iter('img'))
                if img:
                    p = noscript[0].getparent()
                    idx = p.index(noscript[0])
                    p.insert(idx, p.makeelement('img', src=img[0].get('src')))
                    p.remove(noscript[0])
        for x in root.xpath('//*[name()="script" or name()="style" or name()="source" or name()="meta"]'):
            x.getparent().remove(x)
        # the economist uses <small> for small caps with a custom font
        for init in root.xpath('//span[@data-caps="initial"]'):
            init.set('style', 'font-weight:bold;')
        for x in root.xpath('//small'):
            if x.text and len(x) == 0:
                x.text = x.text.upper()
                x.tag = 'span'
                x.set('style', 'font-variant: small-caps')
        for h2 in root.xpath('//h2'):
            h2.tag = 'h4'
        for x in root.xpath('//figcaption'):
            x.set('style', 'text-align:center; font-size:small;')
        for x in root.xpath('//cite'):
            x.tag = 'blockquote'
            x.set('style', 'color:#404040;')
        raw = etree.tostring(root, encoding='unicode')
        return raw

        raw_ar = read_url([], 'https://archive.is/latest/' + url)
        archive = BeautifulSoup(str(raw_ar))
        art = archive.find('article')
        if art:
            bdy = art.findAll('section')
            if len(bdy) != 0:
                content = bdy[-1]
            else:
                content = archive.find('div', attrs={'itemprop':'text'})
            soup = BeautifulSoup(raw)
            article = soup.find('section', attrs={'id':'body'})
            if not article:
                article = soup.find('div', attrs={'itemprop':'text'})
                if not article:
                    article = soup.find(attrs={'itemprop':'blogPost'})
            if article and content:
                self.log('**fetching archive content')
                article.append(content)

                div = soup.findAll(attrs={'style': lambda x: x and x.startswith(
                        ('color:rgb(13, 13, 13);', 'color: rgb(18, 18, 18);')
                    )})
                for p in div:
                    p.name = 'p'
                return str(soup)
            return raw
        return raw

    def preprocess_web_html(self, soup):
        for img in soup.findAll('img', attrs={'old-src':True}):
            img['src'] = img['old-src']
        for a in soup.findAll('a', href=True):
            a['href'] = 'http' + a['href'].split('http')[-1]
        for fig in soup.findAll('figure'):
            fig['class'] = 'sub'
        for sty in soup.findAll(attrs={'style':True}):
            del sty['style']
        width = '600'
        w = self.recipe_specific_options.get('res')
        if w and isinstance(w, str):
            width = w
        for img in soup.findAll('img', src=True):
            if '/cdn-cgi/image/' not in img['src']:
                qua = 'economist.com/cdn-cgi/image/width=' + width + ',quality=80,format=auto/'
                img['src'] = img['src'].replace('economist.com/', qua)
            else:
                img['src'] = re.sub(r'width=\d+', 'width=' + width, img['src'])
        return soup