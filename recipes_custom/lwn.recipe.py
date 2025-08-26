#!/usr/bin/env python
# vim:fileencoding=utf-8
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from calibre.web.feeds.news import BasicNewsRecipe


class LWNFree(BasicNewsRecipe):
    title = 'LWN Linux Weekly News (Free)'  # Default, will be overridden dynamically
    language = 'en'
    __author__ = 'yodha8'
    description = "LWN is published every Thursday. This recipe skips current week's articles (subscriber-only) and pulls free articles from previous week."
    oldest_article = 28  # So we can grab previous week articles.
    max_articles_per_feed = 100
    simultaneous_downloads = 9
    extra_css = '.FeatureByline { font-size:small; }'
    masthead_url = 'https://www.socallinuxexpo.org/sites/default/files/logos/lwn-logo-541x179.png'
    keep_only_tags = [dict(name='div', attrs={'class':['ArticleText', 'PageHeadline']})]
    remove_tags = [dict(name='blockquote', attrs={'class':'ad'}), dict(name='form')]

    feeds = [
        ('LWN Articles', 'https://lwn.net/headlines/Features'),
    ]
    cover_url = masthead_url  # Use masthead image for cover
    
    def parse_feeds(self):
        '''Remove paid articles and articles older than a week. Set ebook title from current issue.'''

        prev_feeds = super().parse_feeds()

        remove_articles = []
        weekly_count = 0
        issue_title = None

        for article in prev_feeds[0]:
            # Paid article
            if '[$]' in article.title:
                remove_articles.append(article)
                continue

            # Find the first free Weekly Edition title
            if 'Weekly Edition' in article.title and not issue_title:
                issue_title = article.title

            # Count how many free weekly edition we passed
            if 'Weekly Edition' in article.title:
                weekly_count += 1
                remove_articles.append(article)

            # Remove all articles starting from 2nd free weekly edition
            if weekly_count > 1:
                remove_articles.append(article)

        # Remove everything but prev week's free articles
        for pa in remove_articles:
            prev_feeds[0].remove_article(pa)

        # Set ebook title from issue name if found
        if issue_title:
            self.title = issue_title
        else:
            self.title = 'LWN Linux Weekly News (Free)'

        return prev_feeds
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
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
        except Exception:
            font = ImageFont.load_default()
        # Split title into multiple lines if too long
        title_text = self.title
        max_chars = 15
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
        line_spacing = 7
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
