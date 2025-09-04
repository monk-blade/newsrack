#!/usr/bin/env  python

from calibre.web.feeds.news import BasicNewsRecipe, classes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io, re
import mechanize
calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
_name = '0.Daily Affairs'

class DailyCurrentAffairs(BasicNewsRecipe):
    title = _name + ' - ' + datetime.now().strftime('%d.%m.%y')
    description = 'Daily Affairs related Articles.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 1.2  # days
    max_articles_per_feed = 50
    encoding = 'utf-8'
    use_embedded_content = True
    #masthead_url = 'https://d3jlwjv6gmyigl.cloudfront.net/assets/two/images/logo-2d6831bc63e1ecb76091541e2f20069a.png'
    no_stylesheets = True
    remove_attributes = ['style', 'height', 'width']
    ignore_duplicate_articles = {'url'}
    compress_news_images = True
    compress_news_images_auto_size = 12
    scale_news_images = (800, 800)
    simultaneous_downloads = 9


    extra_css = """
    body {
        font-size: 1em !important;
        line-height: 1.6 !important;
        margin: 0.5em !important;
        background: #fff !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: bold !important;
        margin-top: 0.7em !important;
        margin-bottom: 0.4em !important;
        line-height: 1.2 !important;
    }
    h1 { font-size: 1.2em !important; }
    h2 { font-size: 1.1em !important; }
    h3 { font-size: 1.05em !important; }
    h4, h5, h6 { font-size: 1em !important; }
    p, li {
        font-size: 1em !important;
        margin-top: 0.3em !important;
        margin-bottom: 0.3em !important;
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
        color: #1a0dab !important;
        text-decoration: underline !important;
        word-break: break-all !important;
    }
    """
    remove_tags = [
        dict(name='a', attrs={'href': lambda x: x and 'linkedin.com' in x}),
        dict(name='a', attrs={'href': lambda x: x and 'enrollment' in x}),
        # dict(name='img', attrs={'src': lambda x: x and 'images/img' in x and any(keyword in x for keyword in ['promotion', 'ad', 'banner'])}),
        classes('image-link-expand'),
        # dict(name='div', attrs={'id':'subs-popup-banner'}),
    #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
    ]

    # remove_tags_after = [
    #     dict(name='h5', attrs={'class': lambda x: x and 'heading' in x.lower()}),  # Remove everything after sponsor heading
    #     dict(name='h5', string=lambda s: s and 'message from our sponsor' in s.lower()),
    # ]

    feeds = [
        ('Finshots-AI','https://monk-blade.github.io/scripts-rss/processed-Q_Fin.xml'),
        ('IE Explained-AI','https://monk-blade.github.io/scripts-rss/processed-Explained__IE.xml'),
        ('Mint Opinions-AI','https://monk-blade.github.io/scripts-rss/processed-Q_mint_oped.xml'),
        ('Masala Chai', 'https://rss.beehiiv.com/feeds/Jk0t0xwJeq.xml'),
        ('The Daily Brief by Zerodha', 'https://thedailybrief.zerodha.com/feed'),
        ('The Core', 'https://rss.beehiiv.com/feeds/4BOnz8D132.xml'),
        ('Public Policy' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=f781f37f49c75d5e12d31bf2610d0d54&f=rss'),
        ('India Wants to Know', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=5d2a22d418134e27d410bac251a9e307&f=rss'),
        ('Last Week in AI' ,'https://lastweekin.ai/feed'),
        ('Daily OpEds','https://afeias.com/knowledge-centre/feed/'),
        ('The Hindu OpEd','https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=403b016ea7274f8e856ce18043cccd1b&f=rss'),
        ('CivilsDaily' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=493f596d8391aa0893413b695b1f564f&f=rss'),   
        ('DrishtiIAS Hindi CA', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=1f811be00e94cbb77e7ebed5b70c97c2&f=rss'),
        ('Word of the day','https://www.merriam-webster.com/wotd/feed/rss2'),
        # ('Money', 'https://finshots.in/tag/money/rss/'),
        # ('Insights', 'https://www.insightsonindia.com/category/current-affairs-2/feed/'),
        # ('IASbaba', 'https://iasbaba.com/iasbabas-daily-current-affairs/feed/'),
        # ('9PM Brief ForumIAS','https://blog.forumias.com/category/9-pm-brief/feed/'),
        # ('Newspaper Clips', 'https://afeias.com/knowledge-centre/newspaper-clips/feed/'),
        # ('7PM Editorial ForumIAS', 'https://blog.forumias.com/category/7-pm/feed/'),
        ]

    def default_cover(self, cover_file):
        """
        Create a generic cover for recipes that don't have a cover
        This override adds time to the cover
        """
        try:
            # Create a new image with a light gray background
            width, height = 800, 1200
            background_color = (240, 240, 240)  # Light gray
            image = Image.new('RGB', (width, height), background_color)
            draw = ImageDraw.Draw(image)

            # Define the text
            middle_text = "Daily Affairs"
            date_text = datetime.now().strftime("%d %B %Y")
            day_text = datetime.now().strftime("%A")

            # Load fonts - use Linux system fonts
            font_size_middle = 100
            font_size_date = 60  # Increased font size for date
            font_size_day = 50
            
            try:
                # Try common Linux font paths
                font_middle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_middle)
                font_date = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_date)
                font_day = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size_day)
            except OSError:
                try:
                    # Fallback to Liberation fonts
                    font_middle = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size_middle)
                    font_date = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size_date)
                    font_day = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", font_size_day)
                except OSError:
                    # Final fallback to default font
                    font_middle = ImageFont.load_default()
                    font_date = ImageFont.load_default()
                    font_day = ImageFont.load_default()

            # Calculate text size and position using textbbox
            middle_text_bbox = draw.textbbox((0, 0), middle_text, font=font_middle)
            date_text_bbox = draw.textbbox((0, 0), date_text, font=font_date)
            day_text_bbox = draw.textbbox((0, 0), day_text, font=font_day)

            middle_text_width = middle_text_bbox[2] - middle_text_bbox[0]
            middle_text_height = middle_text_bbox[3] - middle_text_bbox[1]
            date_text_width = date_text_bbox[2] - date_text_bbox[0]
            date_text_height = date_text_bbox[3] - date_text_bbox[1]
            day_text_width = day_text_bbox[2] - day_text_bbox[0]
            day_text_height = day_text_bbox[3] - day_text_bbox[1]

            middle_text_position = ((width - middle_text_width) // 2, (height - middle_text_height) // 2)
            date_text_position = ((width - date_text_width) // 2, height - date_text_height - 150)
            day_text_position = ((width - day_text_width) // 2, height - day_text_height - 50)

            # Draw the text on the image
            draw.text(middle_text_position, middle_text, fill="black", font=font_middle)
            draw.text(date_text_position, date_text, fill="black", font=font_date)
            draw.text(day_text_position, day_text, fill="black", font=font_day)

            # Add a border around the image
            border_color = (0, 0, 0)  # Black
            border_width = 10
            draw.rectangle([border_width // 2, border_width // 2, width - border_width // 2, height - border_width // 2], outline=border_color, width=border_width)

            # Add a horizontal line above the date text
            line_y = date_text_position[1] - 20
            draw.line([(50, line_y), (width - 50, line_y)], fill="black", width=3)

            # Download and paste logos using mechanize
            def download_image(url):
                br = mechanize.Browser()
                br.set_handle_robots(False)
                br.addheaders = [('User-agent', 'Mozilla/5.0')]
                br.open(url)
                return Image.open(io.BytesIO(br.response().read()))

            logo1_url = "https://static-asset.inc42.com/civilsdaily.png"
            logo2_url = "https://www.drishtiias.com/hindi/drishti/img/logo.png"
            logo1 = download_image(logo1_url)
            logo2 = download_image(logo2_url)

            # Resize logos
            logo1 = logo1.resize((150, 150))
            logo2 = logo2.resize((150, 150))

            # Ensure logos have an alpha channel
            logo1 = logo1.convert("RGBA")
            logo2 = logo2.convert("RGBA")

            # Paste logos on the image using alpha channel as mask
            image.paste(logo1, (50, 50), logo1)
            image.paste(logo2, (width - 200, 50), logo2)

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

