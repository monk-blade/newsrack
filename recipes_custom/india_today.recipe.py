from calibre.web.feeds.news import BasicNewsRecipe, classes

#TODO Good CSS

_name = 'India Today Magazine'

class IndiaToday(BasicNewsRecipe):
    title = u'India Today Magazine'
    language = 'en_IN'
    __author__ = 'unkn0wn'
    no_stylesheets = True
    use_embedded_content = False
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    description = (
        'India’s Most Reputed, Credible and Popular news magazine.'
        ' Read the most preferred magazine of 9.5 million Indians to access highly researched and unbiased content.'
    )
    masthead_url = 'https://akm-img-a-in.tosshub.com/sites/all/themes/itg/logo.png'

    extra_css = '''
        .body_caption{font-size:small;}
        .image-alt{font-size:small;}
        [itemprop^="description"] {font-size: small; font-style: italic;}
        
    '''

    def get_cover_url(self):
        soup = self.index_to_soup(
            'https://www.readwhere.com/magazine/the-india-today-group/India-Today/1154'
        )
        for citem in soup.findAll(
            'meta', content=lambda s: s and s.endswith('/magazine/300/new')
        ):
            return citem['content'].replace('300', '600')

    keep_only_tags = [
        dict(name='h1'),
        classes('story-kicker story-right'),
        dict(itemProp='articleBody'),
    ]

    def parse_index(self):
        soup = self.index_to_soup('https://www.indiatoday.in/magazine')

        section = None
        sections = {}

        for tag in soup.findAll(
            'div', attrs={'class': ['magazin-top-left', 'section-ordering']}
        ):
            sec = tag.find('span')
            section = self.tag_to_string(sec)
            self.log(section)
            sections[section] = []

            for a in tag.findAll(
                'a',
                href=lambda x: x and x.startswith((
                    "/magazine/cover-story/story/",
                    "https://www.indiatoday.in/magazine/"
                ))
            ):
                url = a['href']
                if url.startswith('https'):
                    url = url
                else:
                    url = 'https://www.indiatoday.in' + url
                title = self.tag_to_string(a).strip()
                try:
                    desc = self.tag_to_string(a.findParent(
                        'span', attrs={'class':'field-content'}).findNext(
                            'div', attrs={'class':'views-field'})).strip()
                except Exception:
                    desc = self.tag_to_string(a.findParent(
                        ('h3','p')).findNext('span', attrs={'class':'kicket-text'})).strip()
                if not url or not title:
                    continue
                self.log('\t', title)
                self.log('\t', desc)
                self.log('\t\t', url)
                sections[section].append({'title': title, 'url': url, 'description': desc})

        def sort_key(x):
            section = x[0]
            try:
                return (
                    'EDITOR\'S NOTE', 'Cover Story', 'The Big Story', 'Upfront',
                    'NATION', 'INTERVIEW'
                ).index(section)
            except Exception:
                return 99999999

        return sorted(sections.items(), key=sort_key)

    def preprocess_raw_html(self, raw_html, url):
        from calibre.ebooks.BeautifulSoup import BeautifulSoup
        soup = BeautifulSoup(raw_html)
        for div in soup.findAll('div', attrs={'id': 'premium_content_data'}):
            div.extract()
        for tv in soup.findAll(
            'div',
            attrs={
                'class': ['live-tv-ico', 'sendros', 'live-tv-ico-st', 'sendros-st']
            }
        ):
            tv.extract()
        for script in soup.findAll('script'):
            script.extract()
        for style in soup.findAll('style'):
            style.extract()
        for img in soup.findAll('img', attrs={'data-src': True}):
            img['src'] = img['data-src']
        for h2 in soup.findAll('h2'):
            h2.name = 'h5'
        return str(soup)
