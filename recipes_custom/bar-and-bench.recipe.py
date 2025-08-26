#!/usr/bin/env python
from datetime import datetime
from calibre.web.feeds.news import BasicNewsRecipe, prefixed_classes
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

class bar(BasicNewsRecipe):
    title = 'Bar and Bench'
    __author__ = 'unkn0wn'
    description = (
        'Bar & Bench is the premier online portal for Indian legal news. News, interviews,'
        ' and columns related to the Supreme Court of India and the High Courts are published.'
        )
    language = 'en_IN'
    masthead_url = 'https://media.assettype.com/barandbench%2F2020-04%2F942d4c3e-b84d-4afe-8e88-b76fd6c1ac34%2FBar_and_Bench_Stacked.png?w=1200&ar=40%3A21&auto=format%2Ccompress&ogImage=true&mode=crop&enlarge=true'
    simultaneous_downloads = 9
    no_stylesheets = True
    remove_javascript = True
    remove_attributes = ['height', 'width', 'style']
    
    keep_only_tags = [
        prefixed_classes(
            'text-story-m_header-details__ text-story-m_hero-image__ text-story-m_story-content-inner-wrapper__'
        )
    ]

    remove_tags = [
        prefixed_classes(
            'text-story-m_story-tags__ story-footer-module__metype__ text-story-m_share__FrlMt'
        ),
        dict(name='svg')
    ]

    def preprocess_html(self, soup):
        for img in soup.findAll('img', attrs={'data-src':True}):
            img['src'] = img['data-src']
        return soup

    ignore_duplicate_articles = {'title'}
    resolve_internal_links  = True
    remove_empty_feeds = True

    def parse_index(self):
        index = 'https://www.barandbench.com/'
        feeds = []
        soup = self.index_to_soup(index)
        
        # Debug: Check if we can fetch the page at all
        self.log("Successfully fetched homepage")
        
        # Collect all articles from the homepage
        all_articles = []
        
        # Strategy 1: Find all links that contain headline elements  
        for a in soup.findAll('a', href=True):
            url = a.get('href')
            if not url or not url.startswith(index):
                continue
                
            # Look for headline elements inside this link
            headline = a.find(['h6', 'h5', 'h2'], class_='headline-m_headline__3_NhV')
            if headline:
                title = headline.get_text(strip=True)
                if title:
                    # Clean URL by removing query parameters and fragments
                    url = url.split('?')[0].split('#')[0]
                    
                    # Skip homepage/section roots
                    if url in [index, index.rstrip('/')]:
                        continue
                        
                    # Determine section based on URL path
                    section = 'Legal News'
                    if '/view-point/' in url:
                        section = 'View-Point'
                    elif '/columns/' in url:
                        section = 'Columns'
                    elif '/interviews/' in url:
                        section = 'Interviews'
                    elif '/news/' in url:
                        section = 'News'
                    
                    self.log(f"Found article: {title} -> {section}")
                    all_articles.append({'title': title, 'url': url, 'section': section})
        
        self.log(f"Total articles found: {len(all_articles)}")
        
        # Group articles by section
        sections = {}
        for article in all_articles:
            section = article['section']
            if section not in sections:
                sections[section] = []
            # Avoid duplicates
            if not any(existing['url'] == article['url'] for existing in sections[section]):
                sections[section].append({'title': article['title'], 'url': article['url']})
        
        # Create feeds from sections
        for section_name, articles in sections.items():
            if articles:  # Only add sections that have articles
                self.log(f"{section_name}: {len(articles)} articles")
                feeds.append((section_name, articles))
        
        # If no articles found, create a fallback with some default content
        if not feeds:
            self.log("No articles found, creating fallback feed")
            fallback_articles = [
                {'title': 'Bar and Bench Homepage', 'url': index}
            ]
            feeds.append(('Legal News', fallback_articles))
                
        return feeds
    def get_cover_url(self):
        '''Generate a custom cover with masthead and title.'''
        # Download masthead image using Calibre's browser
        f = self.browser.open(self.masthead_url, timeout=self.timeout)
        masthead = Image.open(BytesIO(f.read())).convert('RGBA')
        f.close()

        # Set cover size to fixed 800x1200
        cover_width = 800
        cover_height = 1200
        cover = Image.new('RGBA', (cover_width, cover_height), (255, 255, 255, 255))

        # Paste masthead in the top half, centered horizontally
        masthead_max_height = cover_height // 2 - 40
        masthead_scale = min(1.0, masthead_max_height / masthead.height, (cover_width - 40) / masthead.width)
        try:
            resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            resample_method = 3  # BICUBIC fallback
        masthead_resized = masthead.resize((int(masthead.width * masthead_scale), int(masthead.height * masthead_scale)), resample=resample_method)
        masthead_x = (cover_width - masthead_resized.width) // 2
        masthead_y = 40 + (masthead_max_height - masthead_resized.height) // 2
        cover.paste(masthead_resized, (masthead_x, masthead_y), masthead_resized)

        # Draw title in the bottom half
        draw = ImageDraw.Draw(cover)
        try:
            font = ImageFont.truetype("LiberationSans-Bold.ttf", 125)
        except Exception:
            font = ImageFont.load_default()
        # Split title into multiple lines if too long
        title_text = datetime.now().strftime('%d.%m.%y %A')
        max_chars = 8
        words = title_text.split()
        lines = []
        current_line = ''
        for word in words:
            if len(current_line + ' ' + word) <= max_chars:
                if current_line:
                    current_line += ' '
                current_line += word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Calculate total height for all lines
        total_height = 0
        line_heights = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_height = bbox[3] - bbox[1]
            line_heights.append(line_height)
            total_height += line_height

        # Add spacing between lines
        line_spacing = 30
        total_height += line_spacing * (len(lines) - 1)
        # Center text block in bottom half
        start_y = cover_height // 2 + ((cover_height // 2 - total_height) // 2)
        y = start_y
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (cover_width - text_width) // 2
            draw.text((text_x, y), line, fill=(0, 80, 0), font=font)
            y += line_heights[i] + line_spacing

        # Add border using provided example
        border_color = (0, 0, 0)  # Black
        border_width = 5
        bordered_width = cover_width
        bordered_height = cover_height
        bordered_cover = Image.new('RGBA', (bordered_width, bordered_height), (255, 255, 255, 255))
        bordered_cover.paste(cover, (0, 0))
        draw_border = ImageDraw.Draw(bordered_cover)
        draw_border.rectangle(
            [border_width // 2, border_width // 2, bordered_width - border_width // 2, bordered_height - border_width // 2],
            outline=border_color,
            width=border_width
        )

        # Save to temp file
        cover_path = os.path.join(os.getcwd(), 'custom_cover_lwn.png')
        bordered_cover.convert('RGB').save(cover_path, 'PNG')
        return cover_path
