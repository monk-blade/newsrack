#!/usr/bin/env  python
from datetime import date, datetime, timedelta
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
import re
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree
import urllib.request
import urllib.error

_name = 'રસરંગ'
class Rasrang(BasicNewsRecipe):
    title = 'રસરંગ'
    description = 'રસરંગ — curated collection of Gujarati feed items'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 2  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    center_navbar = True
    use_embedded_content = True
    masthead_url = 'https://www.divyabhaskar.co.in/assets/images/logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """

    feeds = [
        ('રસરંગ', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=4f3a45ee1c9ba7c5339f0525726c37e0&f=rss'),
    ]

    def get_cover_url(self):
        """Get the cover image URL for the current Rasrang edition."""
        try:
            # Fetch the epaper page content
            epaper_url = "https://www.divyabhaskar.co.in/epaper"
            
            default_log.info(f"[Rasrang] Fetching cover image from: {epaper_url}")
            
            # Fetch the page content
            req = urllib.request.Request(epaper_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
            
            # Extract the cover image URL using regex
            # Look for pattern: https://images.bhaskarassets.com/thumb/444x294/epaper/gujrat/epaperimages/DDMMYYYY/DDrasrang-pg1-0.jpg
            img_pattern = r'https://images\.bhaskarassets\.com/thumb/444x294/epaper/gujrat/epaperimages/[^"]*rasrang-pg1-0\.jpg'
            match = re.search(img_pattern, content)
            
            if match:
                cover_url = match.group(0)
                # Convert to higher resolution (1200x800 instead of 444x294)
                high_res_cover_url = cover_url.replace('/thumb/444x294/', '/thumb/800x1200/')
                default_log.info(f"[Rasrang] Found cover image URL: {high_res_cover_url}")
                return high_res_cover_url
            else:
                default_log.warning(f"[Rasrang] Could not find cover image in page content")
                # Try alternative pattern matching for rasrang
                alt_pattern = r'https://images\.bhaskarassets\.com/[^"]*rasrang[^"]*\.jpg'
                alt_match = re.search(alt_pattern, content)
                if alt_match:
                    alt_cover_url = alt_match.group(0)
                    # Convert to higher resolution if it has thumb path
                    if '/thumb/444x294/' in alt_cover_url:
                        alt_cover_url = alt_cover_url.replace('/thumb/444x294/', '/thumb/1200x800/')
                    default_log.info(f"[Rasrang] Found alternative cover image URL: {alt_cover_url}")
                    return alt_cover_url
                
                # Fallback to masthead
                return self.masthead_url
                
        except Exception as e:
            default_log.error(f"[Rasrang] Error fetching cover image: {str(e)}")
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
        default_log.info(f"[Rasrang] Article: '{article.title}' | Words: {word_count} | Reading time: {minutes}m")
        default_log.info(f"[Rasrang] Content preview: {' '.join(words[:30])}")
        
        # Update article title with reading time if not already present
        if not re.search(r" \(\d+m\)$", article.title or ''):
            article.title = f"{article.title} ({minutes}m)"
            default_log.info(f"[Rasrang] Updated title: {article.title}")

    def preprocess_html(self, soup):
        """Basic HTML preprocessing."""
        return soup
