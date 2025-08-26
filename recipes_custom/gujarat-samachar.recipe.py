import os, sys
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe
from datetime import date, datetime
from calibre.web.feeds.news import BasicNewsRecipe,classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree
from PIL import Image, ImageDraw, ImageFont
import io
import mechanize

_name = 'News of Gujarat'
class GujaratSamachar(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    description = 'News of Gujarat is compilation of various feeds of Gujarati Paper'
    language = 'gu'
    __author__ = 'Arpan'
    oldest_article = 1.25  # days
    max_articles_per_feed = 50
    summary_length = 175
    publication_type = "newspaper"
    encoding = 'utf-8'
    use_embedded_content = True
    simultaneous_downloads = 9
    masthead_url = 'https://www.gujaratsamachar.com/assets/logo.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """

    feeds = [
        ('Sandesh | Opinion', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=a2abf353cf0a8c508fb6c10f36856ad9&f=rss'),
        ('GS | Editorials', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=93efd7f00ba0514c11e60494b70edd44&f=rss'),
        ('ઓરિજનલ | દિવ્યભાસ્કર', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=7a0609bc4ecc4fbadaf1c9c831ac62a1&f=rss'),
        ('ગુજરાતી પૂર્તિઓ' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=6d573adee7f766e07d3cbd8b8d4fee40&f=rss'),
    ]

    def download_google_font(self, font_family, font_weight=400):
        """Download Google Font and return font path"""
        try:
            # Create fonts directory if it doesn't exist
            fonts_dir = "/tmp/fonts"
            os.makedirs(fonts_dir, exist_ok=True)
            
            # Google Fonts API URL
            font_url = f"https://fonts.googleapis.com/css2?family={font_family}:wght@{font_weight}&display=swap"
            
            # Get CSS content using Calibre's browser
            br = self.get_browser()
            response = br.open(font_url)
            css_content = response.read().decode('utf-8')
            
            # Extract font file URL from CSS
            import re
            font_file_match = re.search(r'url\((https://[^)]+\.woff2)\)', css_content)
            
            if font_file_match:
                font_file_url = font_file_match.group(1)
                font_response = br.open(font_file_url)
                font_data = font_response.read()
                
                font_path = os.path.join(fonts_dir, f"{font_family}_{font_weight}.woff2")
                with open(font_path, 'wb') as f:
                    f.write(font_data)
                
                return font_path
            
        except Exception as e:
            self.log.warning(f"Failed to download Google Font: {e}")
        
        return None

    def default_cover(self, cover_file):
        """
        Create an exciting and relevant cover for Gujarati news publication
        """
        try:
            # Create a new image with vibrant gradient background
            width, height = 800, 1200
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            
            # Create gradient background (saffron to white to green - Indian flag colors)
            for y in range(height):
                if y < height // 3:
                    # Saffron gradient
                    ratio = y / (height // 3)
                    r = int(255 - (255 - 255) * ratio)
                    g = int(153 - (153 - 200) * ratio)
                    b = int(51 - (51 - 100) * ratio)
                elif y < 2 * height // 3:
                    # White section
                    r, g, b = 255, 255, 255
                else:
                    # Green gradient
                    ratio = (y - 2 * height // 3) / (height // 3)
                    r = int(255 - (255 - 19) * ratio)
                    g = int(255 - (255 - 136) * ratio)
                    b = int(255 - (255 - 8) * ratio)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b))

            # Define the text
            main_title = "ગુજરાતના સમાચાર"  # News of Gujarat
            date_text = datetime.now().strftime("%d %B %Y")
            day_text = datetime.now().strftime("%A")

            # Font sizes
            font_size_title = 100
            font_size_date = 60
            font_size_day = 50
            
            # Try to download and use Google Font Rasa
            rasa_font_path = self.download_google_font("Rasa", 700)  # Bold weight
            
            try:
                if rasa_font_path and os.path.exists(rasa_font_path):
                    # Use downloaded Rasa font
                    font_title = ImageFont.truetype(rasa_font_path, font_size_title)
                else:
                    raise OSError("Rasa font not available")
                    
                # For date and day, try system fonts that support Gujarati
                font_date = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_date)
                font_day = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_day)
            except Exception as e:
                self.log.warning(f"Failed to load fonts: {e}")
            # Calculate text sizes and positions
            title_bbox = draw.textbbox((0, 0), main_title, font=font_title)
            date_bbox = draw.textbbox((0, 0), date_text, font=font_date)
            day_bbox = draw.textbbox((0, 0), day_text, font=font_day)

            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            date_width = date_bbox[2] - date_bbox[0]
            date_height = date_bbox[3] - date_bbox[1]
            day_width = day_bbox[2] - day_bbox[0]
            day_height = day_bbox[3] - day_bbox[1]

            # Position texts strategically
            title_y = height // 3
            title_position = ((width - title_width) // 2, title_y)
            
            # Position date and day in the bottom section
            date_y = height - 200
            day_y = date_y + date_height + 15
            
            date_position = ((width - date_width) // 2, date_y)
            day_position = ((width - day_width) // 2, day_y)

            # Add decorative elements
            # Draw a semi-transparent overlay for better text readability
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Add decorative rectangle behind title
            title_rect_margin = 20
            overlay_draw.rectangle([
                title_position[0] - title_rect_margin,
                title_position[1] - 10,
                title_position[0] + title_width + title_rect_margin,
                title_position[1] + title_height + 10
            ], fill=(255, 255, 255, 180))
            
            # Date background
            date_rect_margin = 20
            # Calculate the full area needed for both date and day text
            max_text_width = max(date_width, day_width)
            background_left = min(date_position[0], day_position[0]) - date_rect_margin
            background_right = max(date_position[0] + date_width, day_position[0] + day_width) + date_rect_margin
            background_top = date_position[1] - 15
            background_bottom = day_position[1] + day_height + 15
            
            overlay_draw.rectangle([
                background_left,
                background_top,
                background_right,
                background_bottom
            ], fill=(0, 0, 0, 150))
            
            # Composite the overlay
            image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')
            draw = ImageDraw.Draw(image)

            # Draw the text with vibrant colors
            draw.text(title_position, main_title, fill=(0, 51, 102), font=font_title)  # Dark blue
            draw.text(date_position, date_text, fill=(255, 255, 255), font=font_date)  # White
            draw.text(day_position, day_text, fill=(255, 255, 255), font=font_day)  # White

            # Add decorative border and elements
            border_color = (255, 153, 51)  # Saffron
            border_width = 8
            draw.rectangle([
                border_width // 2, border_width // 2, 
                width - border_width // 2, height - border_width // 2
            ], outline=border_color, width=border_width)
            
            # Add corner decorations
            corner_size = 50
            # Top left
            draw.polygon([
                (border_width, border_width),
                (corner_size + border_width, border_width),
                (border_width, corner_size + border_width)
            ], fill=border_color)
            
            # Top right
            draw.polygon([
                (width - border_width, border_width),
                (width - corner_size - border_width, border_width),
                (width - border_width, corner_size + border_width)
            ], fill=border_color)
            
            # Bottom left
            draw.polygon([
                (border_width, height - border_width),
                (corner_size + border_width, height - border_width),
                (border_width, height - corner_size - border_width)
            ], fill=border_color)
            
            # Bottom right
            draw.polygon([
                (width - border_width, height - border_width),
                (width - corner_size - border_width, height - border_width),
                (width - border_width, height - corner_size - border_width)
            ], fill=border_color)

            # Add a central decorative line
            line_y = title_y + title_height + 80
            draw.line([(100, line_y), (width - 100, line_y)], fill=(255, 153, 51), width=4)

            # Save the image to a bytes buffer
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_data = img_buffer.getvalue()

            # Write the image data to the cover file
            cover_file.write(img_data)
            cover_file.flush()
            
        except Exception as e:
            self.log.exception('Failed to generate default cover: %s' % str(e))
            return False
        return True