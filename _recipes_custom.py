from typing import List

from _recipe_utils import (
    CoverOptions,
    Recipe,
    first_n_days_of_month,
    last_n_days_of_month,
    onlyat_hours,
    onlyon_days,
    onlyon_weekdays,
)

# Define the categories display order, optional
categories_sort: List[str] = ["News","Gujarati Supplements","Technology","Newsletters","Indian Magazines","Intl Magazines","Legal"]

# Define your custom recipes list here
# Example: https://github.com/ping/newsrack-fork-test/blob/custom/_recipes_custom.py

recipes: List[Recipe] = [
    Recipe(
        recipe="live-mint",
        slug="live-mint",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        retry_attempts=1,
        overwrite_cover=False,
        enable_on=onlyat_hours(list(range(0, 9)), +5.5),
    ),
    Recipe(
        recipe="hindu",
        slug="hindu",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        retry_attempts=1,
        overwrite_cover=False,
        # timeout=300,
        enable_on=onlyat_hours(list(range(0, 9)), +5.5),  
    ),
    Recipe(
        recipe="business-standard",
        slug="business-standard",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        overwrite_cover=False,
        enable_on=onlyat_hours(list(range(0, 9)), +5.5),
    ),
    Recipe(
        recipe="indian-express",
        slug="indian-express",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        overwrite_cover=False,
        enable_on=onlyat_hours(list(range(0, 9)), +5.5),
    ),
    Recipe(
        recipe="upvote",
        slug="upvote",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        cover_options=CoverOptions(
            border_width=10,
            text_colour="black",  # or in hex format, e.g. "#000000"
            background_colour="white",  # or in hex format, e.g. "#FFFFFF"
            title_font_path="static/OpenSans-Bold.ttf",  # you can define your own font path
            # title_font_size=80,
            datestamp_font_path="static/OpenSans-Semibold.ttf",
            # datestamp_font_size=72,
            logo_path_or_url="https://www.digital-adoption.com/wp-content/uploads/2019/06/Hacker-News-logo.png",
        ),
       enable_on=onlyat_hours(list(range(0, 9)), +5.5),  
    ),

    Recipe(
        recipe="daily-current",
        slug="daily-current",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        retry_attempts=1,
        overwrite_cover=False,
        enable_on=onlyat_hours(list(range(0, 9)), +5.5),
    ),

    Recipe(
        recipe="gujarat-samachar",
        slug="gujarat-samachar",
        src_ext="mobi",
        target_ext=["epub"],
        category="News",
        overwrite_cover=False,
       enable_on=onlyat_hours(list(range(6, 12)), +5.5),
    ),
    Recipe(
        recipe="ravi-purti",
        slug="ravi-purti",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Supplements",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([6]),  # Sunday only
    ),
    Recipe(
        recipe="shatdal-poorti",
        slug="shatdal-poorti",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Supplements",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2]),  # Wednesday only
    ),
    Recipe(
        recipe="ardha-saptahik",
        slug="ardha-saptahik",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Supplements",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2]),  # Wednesday only
    ),
    Recipe(
        recipe="sanskar",
        slug="sanskar",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Supplements",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([6]),  # Sunday only
    ),
    Recipe(
        recipe="rasrang",
        slug="rasrang",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Supplements",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([6]),  # Sunday only
    ),
    Recipe(
        recipe="kalash",
        slug="kalash",
        src_ext="mobi",
        target_ext=["epub"],
        category="Gujarati Supplements",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2]),  # Wednesday only
    ),
    Recipe(
        recipe="newsletters",
        slug="newsletters",
        src_ext="mobi",
        target_ext=["epub"],
        category="Newsletters",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([1,3,5,6]), 
#        enable_on=onlyat_hours(list(range(0, 9)), +5.5),
    ),

    Recipe(
        recipe="frontline",
        slug="frontline",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian Magazines",
        overwrite_cover=False,
       enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="outlook_india",
        slug="outlook_india",
        src_ext="mobi",
        target_ext=["epub"],
        category="Indian Magazines",
        overwrite_cover=False,
        enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="india_today",
        slug="india_today",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),

    Recipe(
        recipe="epw",
        slug="epw",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Indian Magazines",
        enable_on=onlyon_weekdays([6]),  
    ),
    Recipe(
        recipe="bar-and-bench",
        slug="bar-and-bench",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Legal",
        enable_on=onlyon_weekdays([3,6]),
#        enable_on=onlyon_days([1, 14]),   # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="new-scientist",
        slug="new-scientist",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        overwrite_cover=True,
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -5),
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/New_Scientist_logo.svg/1024px-New_Scientist_logo.svg.png"
        ),
    ),
    Recipe(
        recipe="atlantic-magazine",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4),
        tags=["editorial", "commentary"],
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/The_Atlantic_Logo_11.2019.svg/1200px-The_Atlantic_Logo_11.2019.svg.png"
        ),
    ),
    Recipe(
        recipe="thediplomat",
        name="The Diplomat",
        slug="the-diplomat",
        src_ext="mobi",
        target_ext=["epub"],
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5]) and onlyat_hours(list(range(0, 9))),
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/The_Diplomat_logo.svg/1024px-The_Diplomat_logo.svg.png"
        ),
    ),
    Recipe(
        recipe="sc-am",
        slug="sc-am",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Science",
        # timeout=240,
        # enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], 5.5),
    ),
    Recipe(
        recipe="economist",
        slug="economist",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=onlyon_weekdays([6]),
        # timeout=240,
        # enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], 5.5),
    ),
    Recipe(
        recipe="philosophy-now",
        slug="philosophy-now",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=onlyon_weekdays([6]),  # Sunday only
    ),
    Recipe(
        recipe="hbr",
        slug="hbr",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=onlyon_weekdays([6]),
        # enable_on=onlyon_days(list(range(1, 1 + 3)) + list(range(32 - 14, 32)), -5),
    ),
    Recipe(
        recipe="foreign-affairs",
        slug="foreign-affairs",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=(first_n_days_of_month(4, -4) or last_n_days_of_month(10, -4))
        and onlyat_hours(list(range(8, 22)), -4),
    ),
    # Recipe(
    #     recipe="harvard-intl-review",
    #     slug="harvard-intl-review",
    #     src_ext="mobi",
    #     target_ext=["epub"],
    #     category="Intl Magazines",
    #     enable_on=onlyat_hours(list(range(11, 15))),
    #     cover_options=CoverOptions(
    #         logo_path_or_url="https://hir.harvard.edu/content/images/2020/12/HIRlogo_crimson-4.png",
    #     ),
    # ),
    Recipe(
        recipe="mit-press-reader",
        slug="mit-press-reader",
        src_ext="mobi",
        target_ext=["epub"],
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4),
        cover_options=CoverOptions(
            text_colour="#444444",
            logo_path_or_url="https://dhjhkxawhe8q4.cloudfront.net/mit-press/wp-content/uploads/2022/03/25123303/mitp-reader-logo_0-scaled.jpg",
        ),
    ),

    Recipe(
        recipe="mit-tech-review",
        slug="mit-tech-review-feed",
        src_ext="mobi",
        target_ext=["epub"],
        category="Technology",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], -4),
        tags=["technology"],
        cover_options=CoverOptions(
            text_colour="#444444",
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/MIT_Technology_Review_modern_logo.svg/1024px-MIT_Technology_Review_modern_logo.svg.png",
        ),
    ),
    Recipe(
        recipe="mit-tech-review-magazine",
        slug="mit-tech-review-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Technology",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(1, 1 + 7)) + list(range(32 - 7, 32)), -5),
        tags=["technology"],
    ),
    Recipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
    ),
    Recipe(
        recipe="lwn",
        slug="lwn",
        src_ext="mobi",
        target_ext=["epub"],
        category="Technology",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([6]),
    ),
    Recipe(
        recipe="restofworld",
        slug="restofworld",
        src_ext="mobi",
        target_ext=["epub"],
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5]) and onlyat_hours(list(range(0, 9))),
        tags=["technology"],
        cover_options=CoverOptions(
            border_width=2,
            text_colour="black",  # or in hex format, e.g. "#000000"
            background_colour="white",  # or in hex format, e.g. "#FFFFFF"
            title_font_path="static/OpenSans-Bold.ttf",  # you can define your own font path
            title_font_size=80,
            datestamp_font_path="static/OpenSans-Semibold.ttf",
            datestamp_font_size=72,
            logo_path_or_url="recipes/logos/row.png",
        ),
    ),
    Recipe(
        recipe="nautilus",
        slug="nautilus",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5]) and onlyat_hours(list(range(0, 9))),
        tags=["science"],
        cover_options=CoverOptions(
            border_width=2,
            text_colour="black",  # or in hex format, e.g. "#000000"
            background_colour="white",  # or in hex format, e.g. "#FFFFFF"
            title_font_path="static/OpenSans-Bold.ttf",  # you can define your own font path
            title_font_size=80,
            datestamp_font_path="static/OpenSans-Semibold.ttf",
            datestamp_font_size=72,
            logo_path_or_url="recipes/logos/nautilus.png",
        ),
    ),
    Recipe(
        recipe="wired",
        slug="wired",
        src_ext="mobi",
        target_ext=["epub"],
        overwrite_cover=True,
        category="Technology",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5]) and onlyat_hours(list(range(0, 9))),
        cover_options=CoverOptions(
            logo_path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Wired_logo.svg/1024px-Wired_logo.svg.png"
        ),
    ),
    Recipe(
        recipe="knowable-magazine",
        slug="knowable-magazine",
        src_ext="mobi",
        target_ext=["epub"],
        category="Science",
        tags=["science"],
        enable_on=onlyon_weekdays([6]),
        cover_options=CoverOptions(
            border_width=2,
            text_colour="black",  # or in hex format, e.g. "#000000"
            background_colour="white",  # or in hex format, e.g. "#FFFFFF"
            title_font_path="static/OpenSans-Bold.ttf",  # you can define your own font path
            title_font_size=80,
            datestamp_font_path="static/OpenSans-Semibold.ttf",
            datestamp_font_size=72,
            logo_path_or_url="recipes/logos/knowable.png",
        ),
    ),
]
