#!/usr/bin/env  python
from datetime import date, datetime, timedelta
from calibre.web.feeds.news import BasicNewsRecipe,classes
import re
from calibre.utils.logging import default_log
import urllib.request
import json

_name = 'સંસ્કાર'
class Sanskar(BasicNewsRecipe):
    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    description = 'સંસ્કાર — Sandesh weekly publication that publishes on Sunday'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 2  # days
    max_articles_per_feed = 50
    summary_length = 175
    encoding = 'utf-8'
    simultaneous_downloads = 9
    use_embedded_content = True
    masthead_url = 'https://www.sandesh.com/assets/logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    extra_css = """
            p{text-align: justify; font-size: 100%}
            .article-image { margin: 10px 0; text-align: center; }
            .article-image img { max-width: 100%; height: auto; }
    """

    feeds = [
        ('સંસ્કાર', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=052fee9cd5d70ed3250932b5fcb5ee77&f=rss'),
    ]

    def get_cover_url(self):
        """Get the cover image URL for the current Sunday's Sanskar edition."""
        try:
            # Get current date
            today = date.today()
            
            # Find the most recent Sunday (or today if it's Sunday)
            days_since_sunday = (today.weekday() - 6) % 7  # Sunday is 6
            if days_since_sunday == 0 and today.weekday() == 6:
                # Today is Sunday
                sunday_date = today
            else:
                # Get the most recent Sunday
                sunday_date = today - timedelta(days=days_since_sunday)
            
            # Format date for the URL (YYYY-MM-DD)
            date_str = sunday_date.strftime("%Y-%m-%d")
            
            # Construct the API URL
            api_url = f"https://new-wapi.sandesh.com/api/v1/e-paper?slug=sanskar&date={date_str}"
            
            default_log.info(f"[Sanskar] Fetching cover image from API: {api_url}")
            
            # Fetch the API response
            req = urllib.request.Request(api_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
            # Parse JSON response
            data = json.loads(content)
            
            # Extract the first photo from the sub array
            if (data.get('status') and 
                data.get('data') and 
                data['data'].get('sub') and 
                len(data['data']['sub']) > 0 and 
                data['data']['sub'][0].get('photo')):
                
                first_photo = data['data']['sub'][0]['photo']
                # Construct the cover URL
                cover_url = f"https://resize-img.sandesh.com/epapercdn.sandesh.com/{first_photo}"
                
                default_log.info(f"[Sanskar] Found cover image URL: {cover_url}")
                return cover_url
            else:
                default_log.warning(f"[Sanskar] Could not find cover image in API response")
                # Fallback to masthead
                return self.masthead_url
                
        except Exception as e:
            default_log.error(f"[Sanskar] Error fetching cover image: {str(e)}")
            # Fallback to masthead
            return self.masthead_url

    def __init__(self, *args, **kwargs):
        BasicNewsRecipe.__init__(self, *args, **kwargs)
        self.article_media_map = {}

    def parse_feeds(self):
        """Parse feeds and extract media content URLs."""
        feeds = BasicNewsRecipe.parse_feeds(self)
        
        # Get the RSS content to extract media URLs
        try:
            feed_url = self.feeds[0][1]  # Get the RSS URL
            import urllib.request
            req = urllib.request.Request(feed_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                rss_content = response.read().decode('utf-8', errors='ignore')
            
            # Extract all media content URLs and their associated article URLs
            item_pattern = r'<item>(.*?)</item>'
            items = re.findall(item_pattern, rss_content, re.DOTALL)
            
            for item in items:
                # Extract article URL
                link_match = re.search(r'<link[^>]*>([^<]+)</link>', item)
                # Extract media content URL
                media_match = re.search(r'<media:content[^>]+url="([^"]+)"[^>]*>', item)
                
                if link_match and media_match:
                    article_url = link_match.group(1).strip()
                    media_url = media_match.group(1)
                    self.article_media_map[article_url] = media_url
                    default_log.info(f"[Sanskar] Mapped media for URL: {article_url} -> {media_url}")
            
            default_log.info(f"[Sanskar] Found {len(self.article_media_map)} articles with media content")
            
        except Exception as e:
            default_log.error(f"[Sanskar] Error parsing RSS for media content: {str(e)}")
        
        return feeds

    def populate_article_metadata(self, article, soup, first):
        """Calculate reading time from actual article content and update article title."""
        # Add media image to the article if available
        if hasattr(article, 'url') and article.url in self.article_media_map:
            media_url = self.article_media_map[article.url]
            default_log.info(f"[Sanskar] Adding media image to article: {article.title}")
            
            # Add image at the beginning of the article
            image_div = soup.new_tag('div', **{'class': 'article-image'})
            img_tag = soup.new_tag('img', src=media_url, alt='સંસ્કાર તસવીર', style='max-width: 100%; height: auto;')
            image_div.append(img_tag)
            
            # Insert at the beginning of the body or first content element
            body = soup.find('body')
            if body:
                body.insert(0, image_div)
                default_log.info(f"[Sanskar] Successfully added media image to article body")
            else:
                # Try to find the first content container
                first_p = soup.find('p')
                if first_p:
                    first_p.insert_before(image_div)
                    default_log.info(f"[Sanskar] Successfully added media image before first paragraph")
        
        # Calculate reading time
        all_text = soup.get_text()
        words = [w for w in all_text.split() if w.strip()]
        word_count = len(words)

        # Calculate reading time (180 words per minute)
        minutes = max(1, (word_count + 179) // 180)
        
        # Log article content info
        default_log.info(f"[Sanskar] Article: '{article.title}' | Words: {word_count} | Reading time: {minutes}m")
        
        # Update article title with reading time if not already present
        if not re.search(r" \(\d+m\)$", article.title or ''):
            article.title = f"{article.title} ({minutes}m)"
            default_log.info(f"[Sanskar] Updated title: {article.title}")

    def preprocess_html(self, soup):
        """Basic HTML preprocessing."""
        return soup

    def preprocess_raw_html(self, raw_html, url):
        """Extract media content from RSS and add images to article content."""
        try:
            # Check if this looks like RSS content and extract media:content
            if '<media:content' in raw_html:
                # Extract media content URL using regex
                media_pattern = r'<media:content[^>]+url="([^"]+)"[^>]*>'
                media_match = re.search(media_pattern, raw_html)
                
                if media_match:
                    image_url = media_match.group(1)
                    default_log.info(f"[Sanskar] Found media content: {image_url}")
                    
                    # Extract the CDATA content
                    cdata_pattern = r'<!\[CDATA\[(.*?)\]\]>'
                    cdata_match = re.search(cdata_pattern, raw_html, re.DOTALL)
                    
                    if cdata_match:
                        article_content = cdata_match.group(1)
                        
                        # Add the image at the beginning of the article content
                        image_html = f'<div class="article-image"><img src="{image_url}" alt="સંસ્કાર તસવીર" /></div>'
                        modified_content = image_html + article_content
                        
                        # Replace the CDATA content with modified content
                        modified_html = raw_html.replace(cdata_match.group(0), f'<![CDATA[{modified_content}]]>')
                        
                        default_log.info(f"[Sanskar] Added image to article content")
                        return modified_html
                    else:
                        # If no CDATA, try to add image to the description section
                        desc_pattern = r'(<description>)(.*?)(</description>)'
                        desc_match = re.search(desc_pattern, raw_html, re.DOTALL)
                        
                        if desc_match:
                            image_html = f'<div class="article-image"><img src="{image_url}" alt="સંસ્કાર તસવીર" /></div>'
                            modified_desc = desc_match.group(1) + image_html + desc_match.group(2) + desc_match.group(3)
                            modified_html = raw_html.replace(desc_match.group(0), modified_desc)
                            default_log.info(f"[Sanskar] Added image to description content")
                            return modified_html
            
            return raw_html
            
        except Exception as e:
            default_log.error(f"[Sanskar] Error in preprocess_raw_html: {str(e)}")
            return raw_html
