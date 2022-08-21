from typing import List

from _recipe_utils import Recipe, onlyon_days, onlyat_hours, onlyon_weekdays

# Define the categories display order, optional
categories_sort: List[str] = ["News","UPSC","Gujarati Newspapers","Newsletters","Indian Magazines","Intl Magazines","Books"]

# Define your custom recipes list here
# Example: https://github.com/ping/newsrack-fork-test/blob/custom/_recipes_custom.py

recipes: List[Recipe] = [
    Recipe(
        recipe="the-hindu",
        slug="the-hindu",
        src_ext="mobi",
        target_ext=[],
        category="News",
        # enable_on=onlyat_hours(list(range(6, 10)), +5),  # from 6am-11.59am daily, for the timezone UTC-5
    ),
    Recipe(
        recipe="indian-express",
        slug="indian-express",
        src_ext="mobi",
        target_ext=[],
        category="News",
        # enable_on=onlyat_hours(list(range(6, 10)), +5),
    ),
    Recipe(
        recipe="live-mint",
        slug="live-mint",
        src_ext="mobi",
        target_ext=[],
        category="News",
        # enable_on=onlyat_hours(list(range(6, 10)), +5),
    ),
    Recipe(
        recipe="daily-current",
        slug="daily-current",
        src_ext="mobi",
        target_ext=[],
        category="UPSC",
        # enable_on=onlyat_hours(list(range(6, 10)), +5),
    ), 
    Recipe(
        recipe="business-standard",
        slug="business-standard",
        src_ext="mobi",
        target_ext=[],
        category="News",
        # enable_on=onlyat_hours(list(range(6, 10)), +5),
    ),
    Recipe(
        recipe="gujarat-samachar",
        slug="gujarat-samachar",
        src_ext="mobi",
        target_ext=[],
        category="Gujarati Newspapers",
        enable_on=onlyat_hours(list(range(6, 12)), +5),
    ),
    Recipe(
        recipe="sandesh",
        slug="sandesh",
        src_ext="mobi",
        target_ext=[],
        category="Gujarati Newspapers",
        enable_on=onlyat_hours(list(range(6, 12)), +5),
    ),
    Recipe(
        recipe="substack-nl",
        slug="substack-nl",
        src_ext="mobi",
        target_ext=[],
        category="Newsletters",
    ),
    Recipe(
        recipe="finshots",
        slug="finshots",
        src_ext="mobi",
        target_ext=[],
        category="Newsletters",
    ),
    Recipe(
        recipe="frontline",
        slug="frontline",
        src_ext="mobi",
        target_ext=[],
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="outlook_india",
        slug="outlook_india",
        src_ext="mobi",
        target_ext=[],
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="india_today",
        slug="india_today",
        src_ext="mobi",
        target_ext=[],
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="epw",
        slug="epw",
        src_ext="mobi",
        target_ext=[],
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),  # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="dte",
        slug="dte",
        src_ext="mobi",
        target_ext=[],
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),   # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="open",
        slug="open",
        src_ext="mobi",
        target_ext=[],
        timeout=180,
        overwrite_cover=True,
        category="Indian Magazines",
        enable_on=onlyon_days([1, 14]),   # only on days 1, 14 of each month
    ),
    Recipe(
        recipe="atlantic-magazine",
        slug="atlantic-magazine",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4], -4)
        and onlyon_days(list(range(32 - 14, 32)), -4),
    ),
    Recipe(
        recipe="thediplomat",
        name="The Diplomat",
        slug="the-diplomat",
        src_ext="mobi",
        target_ext=[],
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], 5.5),
    ),
    Recipe(
        recipe="economist",
        slug="economist",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=False,
        category="Intl Magazines",
        timeout=240,
    ),
    Recipe(
        recipe="hbr",
        slug="hbr",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=False,
        category="Intl Magazines",
        enable_on=onlyon_days(list(range(1, 1 + 3)) + list(range(32 - 14, 32)), -5),
    ),
    Recipe(
        recipe="mit-tech-review",
        slug="mit-tech-review-feed",
        src_ext="mobi",
        target_ext=[],
        category="Intl Magazines",
        enable_on=onlyon_weekdays([0, 1, 2, 3, 4, 5], -4),
    ),
    Recipe(
        recipe="nature",
        slug="nature",
        src_ext="mobi",
        target_ext=[],
        category="Intl Magazines",
        overwrite_cover=False,
        enable_on=onlyon_weekdays([2, 3, 4], 0),
    ),
    Recipe(
        recipe="scientific-american",
        slug="scientific-american",
        src_ext="mobi",
        target_ext=[],
        category="Intl Magazines",
        overwrite_cover=False,
        enable_on=onlyon_days(list(range(15, 31)), -5),  # middle of the month?
    ),
    Recipe(
        recipe="wired",
        slug="wired",
        src_ext="mobi",
        target_ext=[],
        overwrite_cover=True,
        category="Intl Magazines",
    ),
]
