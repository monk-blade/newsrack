#!/usr/bin/env  python
from datetime import date, datetime, timedelta
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
import re
from calibre.utils.logging import default_log
import urllib.request

_name = 'શતદલ'
class ShatdalPoorti(BasicNewsRecipe):
    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    description = 'શતદલ — curated collection of Gujarati feed items'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 2  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    simultaneous_downloads = 9
    use_embedded_content = True
    masthead_url = 'https://www.gujaratsamachar.com/assets/logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """

    feeds = [
        ('શતદલ', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=d7f40917ec974aacae716cc6b1429410&f=rss'),
    ]

    def get_cover_url(self):
        """Get the cover image URL for the current Wednesday's Shatdal edition."""
        try:
            # Get current date
            today = date.today()
            
            # Find the most recent Wednesday (or today if it's Wednesday)
            days_since_wednesday = (today.weekday() - 2) % 7  # Wednesday is 2
            if days_since_wednesday == 0 and today.weekday() == 2:
                # Today is Wednesday
                wednesday_date = today
            else:
                # Get the most recent Wednesday
                wednesday_date = today - timedelta(days=days_since_wednesday)
            
            # Format date for the URL (DD-MM-YYYY)
            date_str = wednesday_date.strftime("%d-%m-%Y")
            
            # Construct the epaper URL
            epaper_url = f"https://epaper.gujaratsamachar.com/shatdal/{date_str}/1"
            
            default_log.info(f"[ShatdalPoorti] Fetching cover image from: {epaper_url}")
            
            # Fetch the page content
            req = urllib.request.Request(epaper_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
            
            # Extract the cover image URL using regex
            # Look for pattern: src="https://epaperstatic.gujaratsamachar.com/epaper/...SHATDAL...-0.jpg"
            img_pattern = r'src="(https://epaperstatic\.gujaratsamachar\.com/epaper/[^"]*SHATDAL[^"]*-0\.jpg)"'
            match = re.search(img_pattern, content)
            
            if match:
                cover_url = match.group(1)
                default_log.info(f"[ShatdalPoorti] Found cover image URL: {cover_url}")
                return cover_url
            else:
                default_log.warning(f"[ShatdalPoorti] Could not find cover image in page content")
                # Fallback to masthead
                return self.masthead_url
                
        except Exception as e:
            default_log.error(f"[ShatdalPoorti] Error fetching cover image: {str(e)}")
            # Fallback to masthead
            return self.masthead_url

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
        default_log.info(f"[ShatdalPoorti] Article: '{article.title}' | Words: {word_count} | Reading time: {minutes}m")
        default_log.info(f"[ShatdalPoorti] Content preview: {' '.join(words[:30])}")
        
        # Update article title with reading time if not already present
        if not re.search(r" \(\d+m\)$", article.title or ''):
            article.title = f"{article.title} ({minutes}m)"
            default_log.info(f"[ShatdalPoorti] Updated title: {article.title}")

    def preprocess_html(self, soup):
        """Basic HTML preprocessing."""
        return soup
