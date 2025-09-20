# Copyright (c) 2022 https://github.com/monk-blade/
#
# This software is released under the GNU General Public License v3.0
# https://opensource.org/licenses/GPL-3.0

import sys
import re
import os
from datetime import datetime, timedelta
from uuid import uuid4


from calibre.web.feeds.news import BasicNewsRecipe
from calibre.utils.logging import default_log

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import (
    BasicNewsrackRecipe,
    format_title,
    get_datetime_format,
    parse_date,
)

_name = '3.Reddit'
class Reddit(BasicNewsRecipe):
    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    description = 'Reddit — curated collection of posts from various subreddits'
    language = 'en'
    __author__ = 'Arpan'
    oldest_article = 1.5  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    simultaneous_downloads = 9
    use_embedded_content = True
    masthead_url = 'https://logoeps.com/wp-content/uploads/2013/03/reddit-vector-logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    extra_css = """
    body {
        font-size: 1em !important;
        line-height: 1.6 !important;
        margin: 0.5em !important;
        font-family: 'DM Sans', 'Hind Vadodara', Arial, sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'DM Sans', 'Hind Vadodara', Arial, sans-serif !important;
        font-weight: bold !important;
        margin-top: 0.7em !important;
        margin-bottom: 0.4em !important;
        line-height: 1.2 !important;
    }
    h1 { font-size: 1.6em !important; }
    h2 { font-size: 1.5em !important; }
    h3 { font-size: 1.45em !important; }
    h4 { font-size: 1.4em !important; }
    h5 { font-size: 1.4em !important; }
    h6 { font-size: 1.4em !important; }
    p, li {
        font-size: 1em !important;
        margin-top: 0.3em !important;
        margin-bottom: 0.3em !important;
    }
    p {
        text-indent: 2em !important;
        text-align: justify !important;
    }
    b, strong {
        font-weight: bold !important;
    }
    i, em {
        font-style: italic !important;
    }
    img {
        max-width: 95vw !important;
        height: auto !important;
        margin: 0.5em auto !important;
        display: block !important;
    }
    hr {
        border: none !important;
        border-top: 1px solid #ccc !important;
        margin: 1em 0 !important;
    }
    a {
        text-decoration: underline !important;
        word-break: break-all !important;
    }
    """

    feeds = [
        ('r/Programming', 'https://monk-blade.github.io/public-xml/feeds/reddit-programming.xml'),
        ('r/Technology', 'https://monk-blade.github.io/public-xml/feeds/reddit-tech.xml'),
        ('r/Science', 'https://monk-blade.github.io/public-xml/feeds/reddit-science.xml'),
        # ('r/WorldNews', 'https://www.reddit.com/r/worldnews/.rss'),
        ('r/52book', 'https://monk-blade.github.io/public-xml/feeds/reddit-52book.xml'),
        ('r/AskScience', 'http://monk-blade.github.io/public-xml/feeds/reddit-askscience.xml'),
        ('r/ELI5', 'https://monk-blade.github.io/public-xml/feeds/reddit-eli5.xml'),
        # ('r/TodayILearned', 'https://www.reddit.com/r/todayilearned/.rss'),
        ('r/India', 'https://monk-blade.github.io/public-xml/feeds/reddit-india.xml'),
        ('r/Economics', 'https://monk-blade.github.io/public-xml/feeds/reddit-economics.xml'),
        ('r/Linux', 'https://monk-blade.github.io/public-xml/feeds/reddit-linux.xml'),
        ('r/RandomThoughts', 'https://monk-blade.github.io/public-xml/feeds/reddit-randomthoughts.xml'),
        ('r/Futurology', 'https://monk-blade.github.io/public-xml/feeds/reddit-futurology.xml'),
        ('r/Singularity', 'https://monk-blade.github.io/public-xml/feeds/reddit-singularity.xml'),
        ('r/SelfHosted', 'https://monk-blade.github.io/public-xml/feeds/reddit-selfhosted.xml'),
        ]
    
    def parse_feeds(self):
        """Parse feeds and return articles without modifying titles yet."""
        return BasicNewsRecipe.parse_feeds(self)

    def populate_article_metadata(self, article, soup, first):
        """
        Calculate reading time from actual article content, update article title,
        and update publication date metadata.
        
        Args:
            article: The article object containing metadata.
            soup: BeautifulSoup object of the article content.
            first: Boolean indicating if this is the first article.
        """
        # Get all text from the article
        all_text = soup.get_text()
        words = [w for w in all_text.split() if w.strip()]
        word_count = len(words)
        
        # Calculate reading time (180 words per minute)
        minutes = max(1, (word_count + 179) // 180)
        
        # Log article content info
        default_log.info(f"[Reddit] Article: '{article.title}' | Words: {word_count} | Reading time: {minutes}m")
        default_log.info(f"[Reddit] Content preview: {' '.join(words[:30])}")
        
        # Update article title with reading time if not already present
        if not re.search(r" \(\d+m\)$", article.title or ''):
            article.title = f"{article.title} ({minutes}m)"
            default_log.info(f"[Reddit] Updated title: {article.title}")

    def preprocess_html(self, soup):
        """Basic HTML preprocessing."""
        return soup