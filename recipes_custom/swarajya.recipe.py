from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'Swarajya'

class SwarajyaMag(BasicNewsRecipe):
    title = _name
    __author__ = 'unkn0wn'
    description = 'Swarajya - a big tent for liberal right of centre discourse that reaches out, engages and caters to the new India.'
    language = 'en_IN'
    no_stylesheets = True
    remove_javascript = True
    use_embedded_content = False
    remove_attributes = ['height', 'width']
    encoding = 'utf-8'

    keep_only_tags = [
        classes('_2PqtR _1sMRD ntw8h author-bio'),
    ]

    remove_tags = [
        classes('_JscD _2r17a'),
    ]
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """


    def preprocess_html(self, soup):
        for img in soup.findAll('img', attrs={'data-src': True}):
            img['src'] = img['data-src'].split('?')[0]
        return soup

    def parse_index(self):
        soup = self.index_to_soup('https://swarajyamag.com/all-issues')
        a = soup.find('a', href=lambda x: x and x.startswith('/issue/'))
        url = a['href']
        self.log('Downloading issue:', url)
        self.cover_url = a.find('img', attrs={'data-src': True})['data-src']
        soup = self.index_to_soup('https://swarajyamag.com' + url)
        ans = []

        for a in soup.findAll(**classes('_2eOQr')):
            url = a['href']
            if url.startswith('/'):
                url = 'https://swarajyamag.com' + url
            title = self.tag_to_string(a)
            d = a.find_previous_sibling('a', **classes('_2nEd_'))
            if d:
                desc = 'By ' + self.tag_to_string(d).strip()
            self.log(title, ' at ', url, '\n', desc)
            ans.append({'title': title, 'url': url, 'description': desc})
        return [('Articles', ans)]
