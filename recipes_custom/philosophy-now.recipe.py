import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre import browser
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

_name = 'Philosophy Now'


class PhilosophyNow(BasicNewsRecipe):

    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    __author__ = 'unkn0wn'
    description = '''Philosophy Now is a lively magazine for everyone
    interested in ideas. It isn't afraid to tackle all the major questions of
    life, the universe and everything. Published every two months, it tries to
    corrupt innocent citizens by convincing them that philosophy can be
    exciting, worthwhile and comprehensible, and also to provide some enjoyable
    reading matter for those already ensnared by the muse, such as philosophy
    students and academics.'''
    language = 'en'
    use_embedded_content = False
    no_stylesheets = True
    remove_javascript = True
    remove_attributes = ['height', 'width', 'style']
    encoding = 'utf-8'
    ignore_duplicate_articles = {'url'}
    simultaneous_downloads = 9
    keep_only_tags = [classes('article_page')]
    remove_tags = [dict(name='div', attrs={'id': 'welcome_box'})]
    conversion_options = {
        'tags' : 'Philosophy, Philosophy Now, Periodical',
        'authors' : 'newsrack',
    }

    def parse_index(self):
        nr_soup = self.index_to_soup("https://holyspiritomb.github.io/newsrack/")
        nr_issue_date = nr_soup.find("li", id="philosophy-now").find("span", class_="title").string[16:]
        soup = self.index_to_soup('https://philosophynow.org/')
        div = soup.find('div', attrs={'id': 'aside_issue_cover'})
        url = div.find('a', href=True)['href']
        issue_date = div.find('p', attrs={'id': 'aside_issue_date'})
        # issue_number = div.find('p', attrs={'id': 'aside_issue_number'})
        # seriesidx = self.tag_to_string(issue_number).split(' ')[1]
        self.log('Issue date found: ', self.tag_to_string(issue_date).strip())
        self.log(self.verbose)
        cleaned_issue_date = self.tag_to_string(issue_date).strip()
        # Setting verbose forces a regeneration
        if self.verbose is not True:
            if nr_issue_date:
                if nr_issue_date == cleaned_issue_date:
                    self.abort_recipe_processing("We have this issue.")
        self.title = f"{_name}: {cleaned_issue_date}"
        # self.log('Added title: ', self.title)
        for issue in div.findAll('div', attrs={'id': 'aside_issue_text'}):
            self.log('Downloading issue:', self.tag_to_string(issue).strip())
            self.series = "Philosophy Now"
            # self.series_index = seriesidx
        cov_url = div.find('img', src=True)['src']
        self.cover_url = 'https://philosophynow.org' + cov_url
        soup = self.index_to_soup('https://philosophynow.org' + url)

        feeds = OrderedDict()

        for h2 in soup.findAll('h2', attrs={'class': 'article_list_title'}):
            articles = []
            a = h2.find('a', href=True)
            url = a['href']
            url = 'https://philosophynow.org' + url
            title = self.tag_to_string(a)
            des = h2.find_next_sibling('p')
            if des:
                desc = self.tag_to_string(des)
            else:
                desc = ""
            h3 = h2.find_previous_sibling('h3')
            section_title = self.tag_to_string(h3).title()
            self.log('\t', title)
            self.log('\t', desc)
            self.log('\t\t', url)
            articles.append({
                'title': title,
                'url': url,
                'description': desc})

            if articles:
                if section_title not in feeds:
                    feeds[section_title] = []
                feeds[section_title] += articles
        ans = [(key, val) for key, val in feeds.items()]
        return ans

    # PN changes the content it delivers based on cookies, so the
    # following ensures that we send no cookies
    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'