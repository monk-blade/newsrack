# Copyright (c) 2022 https://github.com/monk-blade/
#
# This software is released under the GNU General Public License v3.0
# https://opensource.org/licenses/GPL-3.0

import json
import os
import sys

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])

from calibre.web.feeds.news import BasicNewsRecipe

_name = 'Upvote'
class Upvote(BasicNewsRecipe):
    title = _name
    description = 'Upvote — curated collection of tech and social news from Hacker News, Lemmy, and Lobsters'
    language = 'en'
    __author__ = 'Arpan'
    oldest_article = 1.25  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    center_navbar = True
    use_embedded_content = True
    masthead_url = 'https://www.upvote-rss.com/img/logo.svg'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """

    feeds = [
        ('HackerNews Best', 'https://www.upvote-rss.com/?platform=hacker-news&community=beststories&averagePostsPerDay=7&showScore=&content=&summary=&comments=5&view=rss'),
        ('Lemmy Technology', 'https://www.upvote-rss.com/?platform=lemmy&instance=lemmy.world&community=Technology&averagePostsPerDay=7&content=&summary=&comments=5&view=rss'),
        ('Lobsters All', 'https://www.upvote-rss.com/?platform=lobsters&community=all&type=all&score=50&content=&summary=&comments=7&filterOldPosts=7&view=rss'),
        ('HN Ask', 'https://www.upvote-rss.com/?platform=hacker-news&community=askstories&score=20&content=&summary=&comments=10&view=rss'),
        ('OMG! Ubuntu', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=03286255647546a832597c8c99addfa8&f=rss'),
        ('Phoronix' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=2bab43c9dbc153cd7c03ab979ff6c2bf&f=rss'),
        ('This Week in GNOME' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=edde32a423219f4ee7d31f1e06be04c0&f=rss'),
        ('Adventures in KDE', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=477c3220ee5a498a9de1fe5ad2b3ed01&f=rss'),
        ('Announcements | nixOS', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=f5871e449b44927a088b5180c5b3d89f&f=rss'),
        ]

    def parse_feeds(self):
        """Parse feeds and return articles without modifying titles yet."""
        return BasicNewsRecipe.parse_feeds(self)

    def populate_article_metadata(self, article, soup, first):
        """Calculate reading time from actual article content and update article title."""
        # Get all text from the article
        all_text = soup.get_text()
        words = [w for w in all_text.split() if w.strip()]
        word_count = len(words)
        
        # Calculate reading time (180 words per minute)
        minutes = max(1, (word_count + 179) // 180)
        
        # Log article content info
        default_log.info(f"[Upvote] Article: '{article.title}' | Words: {word_count} | Reading time: {minutes}m")
        default_log.info(f"[Upvote] Content preview: {' '.join(words[:30])}")
        
        # Update article title with reading time if not already present
        if not re.search(r" \(\d+m\)$", article.title or ''):
            article.title = f"{article.title} ({minutes}m)"
            default_log.info(f"[Upvote] Updated title: {article.title}")

    def preprocess_html(self, soup):
        """Basic HTML preprocessing."""
        return soup
