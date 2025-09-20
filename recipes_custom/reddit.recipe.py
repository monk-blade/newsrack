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
    oldest_article = 1.25  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    # simultaneous_downloads = 9
    use_embedded_content = True
    masthead_url = 'https://download.logo.wine/logo/Reddit/Reddit-Logo.wine.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True


    feeds = [
        
        ('r/Programming', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=e46116f985f2dda5b18592da3c510a88&f=rss'),
        ('r/Technology', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=b62cc0155fb3e453b9f187ee00bcf999&f=rss'),
        ('r/Science', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=643a4a81253a380ad9abdb5227568d6d&f=rss'),
        # # ('r/WorldNews', 'https://www.reddit.com/r/worldnews/.rss'),
        ('r/52book', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=4166d59344720fe3dcf05f1df9266def&f=rss'),
        ('r/AskScience', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=40c661e02ec20b99072800ba620ebe37&f=rss'),
        ('r/ELI5', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=7dec37bd0a4ca121d5facd262479f213&f=rss'),
        # # ('r/TodayILearned', 'https://www.reddit.com/r/todayilearned/.rss'),
        ('r/India', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=0559e834de2d07f3bf992e20f0b2c52a&f=rss'),
        ('r/Economics', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=c79f29564ad6edebb11f677ce5c804c5&f=rss'),
        ('r/Linux', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=08987d65e5048c805c48e42a586b2b67&f=rss'),
        ('r/RandomThoughts', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=12e9d13080872a1bb068b65c2a11360d&f=rss'),
        ('r/Futurology', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=c4266fec1f0df74d1f5ef77dd32d6690&f=rss'),
        ('r/Singularity', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=e40cf199173af9f95a15d2a886558457&f=rss'),
        ('r/SelfHosted', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=375da6167f528da03ed4130ae7ba4fbf&f=rss'),
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
        """HTML preprocessing to clean up Reddit content."""
        # Remove p tags that contain only non-breaking spaces and whitespace
        for p in soup.find_all('p'):
            text = p.get_text()
            # Check if paragraph contains only non-breaking spaces and regular whitespace
            if text and text.replace('\u00a0', '').replace('&nbsp;', '').strip() == '':
                p.decompose()  # Remove the entire p tag
        
        return soup