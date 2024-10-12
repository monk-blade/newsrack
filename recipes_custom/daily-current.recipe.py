#!/usr/bin/env  python
#TODO fix image in 

from calibre.web.feeds.news import BasicNewsRecipe, classes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import mechanize

_name = 'UPSCDaily'

class UPSCDaily(BasicNewsRecipe):
    title = u'UPSC Daily'
    description = 'UPSC Daily is a daily news source for UPSC aspirants.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 2  # days
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
    # keep_only_tags = [
    #     classes('page-hdng stry-shrt-head img-hgt-blk athr-info tm-stmp stry-bdy'),
    # ]
    extra_css = """
            p{text-align: justify; font-size: 100%}
    """

    # remove_tags = [
    #     classes('social-links site-nav-logo container c-search__form subscribe-main site-foot read-next-feed floating-header-share floating-header'),
    #     dict(name='div', attrs={'id':'subs-popup-banner'}),
    # #     dict(name='section', attrs={'class':'glry-cnt mostvdtm main-wdgt glry-bg'}),
    # ]
    # remove_tags_after = [ classes('stry-bdy')]

    feeds = [
        ('CivilsDaily' ,'https://rss-bridge.org/bridge01/?action=display&bridge=CssSelectorBridge&home_page=https%3A%2F%2Fwww.civilsdaily.com&url_selector=.entry-title+a&url_pattern=%2Fnews%2F.*&content_selector=article&content_cleanup=h1.entry-title%2Ca%5Bhref%3D%22https%3A%2F%2Fbit.ly%2FCivilsdailywebinar%22%5D&title_cleanup=&discard_thumbnail=on&limit=15&format=Atom'),   
        ('DrishtiIAS Hindi CA', 'https://rss-bridge.org/bridge01/?action=display&bridge=CssSelectorBridge&home_page=https%3A%2F%2Fwww.drishtiias.com%2Fhindi%2Fcurrent-affairs-news-analysis-editorials%2F&url_selector=body+%3E+section.article-list+%3E+div.wrapper+%3E+div+%3E+article+%3E+div.row+%3E+div%3Anth-child%281%29+%3E+div+%3E+div+%3E+ul+%3E+li+%3E+a&url_pattern=&content_selector=article&content_cleanup=script%2Ciframe%2C.next-post%2C.tags-new%2C.float-sm%2C%23formcontainer%2C.mobile-ad-banner%2C.btn-group%2C.desktop-ad-banner&title_cleanup=&discard_thumbnail=on&limit=3&format=Mrss'),
        # ('Money', 'https://finshots.in/tag/money/rss/'),
        # ('Civilsdaily','https://monk-blade.github.io/reader-scripts/rss.xml'),
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
            middle_text = "UPSC Daily"
            date_text = datetime.now().strftime("%d %B %Y")
            day_text = datetime.now().strftime("%A")

            # Load fonts
            #font_path = "/Library/Fonts/Times New Roman.ttf"  # Adjust the path to a valid font file on your system
            font_path = "/Library/Fonts/Times New Roman Bold.ttf"  # Adjust the path to a valid bold font file on your system
            font_size_middle = 120
            font_size_date = 65  # Increased font size for date
            font_size_day = 55
            font_middle = ImageFont.truetype(font_path, font_size_middle)
            font_date = ImageFont.truetype(font_path, font_size_date)
            font_day = ImageFont.truetype(font_path, font_size_day)

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
        except:
            self.log.exception('Failed to generate default cover')
            return False
        return True

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
