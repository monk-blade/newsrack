#!/usr/bin/env  python
#TODO fix image in 

from calibre.web.feeds.news import BasicNewsRecipe, classes
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import mechanize
from calibre.ebooks.oeb.base import OEBBook
from calibre.utils.logging import default_log
from lxml import etree
calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
class UPSCDaily(BasicNewsRecipe):
    # title = 'UPSC Daily'
    title = 'Daily Current Affairs'
    description = 'Daily Current Affairs related Articles.'
    language = 'en_IN'
    __author__ = 'Arpan'
    oldest_article = 1.25  # days
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
        ('Finshots-AI','https://monk-blade.github.io/scripts-rss/processed-Q_Fin.xml'),
        ('IE Explained-AI','https://monk-blade.github.io/scripts-rss/processed-Explained__IE.xml'),
        ('Mint Opinions-AI','https://monk-blade.github.io/scripts-rss/processed-Q_mint_oped.xml'),
        ('Daily OpEds','https://afeias.com/knowledge-centre/feed/'),
        ('The Hindu OpEd','https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=403b016ea7274f8e856ce18043cccd1b&f=rss'),
        ('CivilsDaily' ,'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=493f596d8391aa0893413b695b1f564f&f=rss'),   
        ('DrishtiIAS Hindi CA', 'https://reader.websitemachine.nl/api/query.php?user=arpanchavdaeng&t=1f811be00e94cbb77e7ebed5b70c97c2&f=rss'),
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
            middle_text = "UPSC Daily"
            date_text = datetime.now().strftime("%d %B %Y")
            day_text = datetime.now().strftime("%A")

            # Load fonts - use Linux system fonts
            font_size_middle = 120
            font_size_date = 65  # Increased font size for date
            font_size_day = 55
            
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

    # def postprocess_book(self, oeb, opts, log):
    #     # Iterate over each item in the manifest
    #     for item in oeb.manifest.items:
    #         log.info(f"File Name: {item.href}")
    #         if item.media_type == 'text/html':
    #             # Access the content of the item
    #             soup = item.data
    #             # Ensure soup is an lxml element
    #             if isinstance(soup, etree._Element):
    #                 # Convert the lxml element to a string for processing
    #                 html_content = etree.tostring(soup, pretty_print=True, encoding='unicode')
    #                 # Parse the HTML content with lxml
    #                 parser = etree.HTMLParser()
    #                 tree = etree.fromstring(html_content, parser)
                    
    #                 # Find all <p> tags using XPath
    #                 p_tags = tree.xpath('//p')
                    
    #                 # Iterate through the <p> tags
    #                 for p in p_tags:
    #                     # Check if the <p> tag contains the specified string
    #                     if "This article was downloaded by" in ''.join(p.xpath('.//text()')):
    #                         # Remove the <p> tag from the HTML content
    #                         p.getparent().remove(p)
                    
    #                 # Find the h2 tag and the div with class calibre_navbar1 using XPath
    #                 h2_tag = tree.xpath('//h1')
    #                 div_tag = tree.xpath('//div[@class="calibre_navbar"]')
                    
    #                 if h2_tag and div_tag:
    #                     h2_tag = h2_tag[0]
    #                     div_tag = div_tag[0]
    #                     # Get the parent of both tags
    #                     parent = h2_tag.getparent()
    #                     # Ensure both elements have the same parent
    #                     if parent == div_tag.getparent():
    #                         # Remove both tags from the parent
    #                         parent.remove(h2_tag)
    #                         parent.remove(div_tag)
    #                         # Reinsert the tags in the desired order
    #                         parent.insert(0, h2_tag)
    #                         parent.insert(1, div_tag)
                    
    #                 # Convert the modified tree back to a string
    #                 modified_html = etree.tostring(tree, pretty_print=True, encoding='unicode')
    #                 # Parse the modified HTML back to an lxml element
    #                 soup = etree.fromstring(modified_html)
                    
    #                 # Update the item data with the modified HTML content
    #                 item.data = soup
    #             else:
    #                 log.error("The soup object is not an lxml element.")
