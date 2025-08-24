# Newsrack Copilot Instructions

## Project Overview
Newsrack is an automated e-book generation system that converts news websites and periodicals into EPUB/MOBI files for e-readers. It uses Calibre recipes (Python classes) to scrape content, GitHub Actions for automation, and serves content via OPDS feeds and GitHub Pages.

## Architecture
- **Recipes**: Python classes in `recipes/` (built-in) and `recipes_custom/` (user-defined) that inherit from Calibre's `BasicNewsRecipe`
- **Core Generation**: `_generate.py` orchestrates recipe execution, file processing, and OPDS catalog generation
- **Recipe Configuration**: `_recipes.py` (default) and `_recipes_custom.py` define recipe metadata, scheduling, and output formats
- **Shared Components**: `recipes/includes/recipes_shared.py` provides `BasicNewsrackRecipe` base class with common utilities
- **Build System**: `build.sh` copies recipes, compiles assets, and runs the generation pipeline
- **GitHub Actions**: `.github/workflows/build.yml` runs daily builds and deploys to GitHub Pages

## Key Development Patterns

## Main Calibre Basic Recipe 
Use https://manual.calibre-ebook.com/_modules/calibre/web/feeds/news.html page to fetch relevant functions and use recipes folder to get idea of calibre recipe development environment.

### Recipe Development
```python
# Standard recipe structure in recipes_custom/
import os, sys
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe

class MyPublication(BasicNewsrackRecipe, BasicNewsRecipe):
    title = "Publication Name"
    # Avoid browser_type = 'webengine' - causes GPU/OpenGL issues in CI
    # Use default mechanize browser instead
```

### Recipe Configuration
```python
# In _recipes_custom.py
Recipe(
    recipe="my-publication",  # matches filename without .recipe.py
    slug="my-publication",    # URL-safe identifier
    src_ext="mobi",          # source format (epub/mobi)
    target_ext=["epub"],     # additional formats to generate
    category="News",         # display category
    enable_on=onlyat_hours(list(range(6, 10)), +5.5),  # timezone-aware scheduling
    retry_attempts=1,        # failure handling
    timeout=300             # seconds
)
```

### Testing Recipes
```bash
# Test individual recipe (uses test_recipe.sh)
./test_recipe.sh -r recipes_custom/my-publication.recipe.py

# Set environment for recipe includes
export recipes_includes=$(realpath recipes/includes/)
```

### Debugging Common Issues
- **WebEngine failures**: Remove `browser_type = 'webengine'` from recipes, use default mechanize
- **Missing dependencies**: Install ALSA libraries (`sudo apt install libasound2-dev libasound2t64`) for Qt components
- **Recipe import errors**: Ensure `recipes_includes` environment variable points to `recipes/includes/`
- **Timeout issues**: Increase `timeout` in recipe configuration, not in recipe class

## Build & Deployment Workflow
1. **Recipe Processing**: `build.sh` copies `.recipe.py` files to `.recipe` format for Calibre
2. **Asset Compilation**: Babel transpiles JS, Sass compiles CSS
3. **Content Generation**: `_generate.py` runs enabled recipes, creates OPDS catalogs
4. **Static Site**: HTML minification, search index generation, GitHub Pages deployment

## File Structure
- `recipes/`: Built-in recipes (don't modify)
- `recipes_custom/`: Your custom recipes
- `_recipes_custom.py`: Configuration for custom recipes
- `static/`: CSS/JS assets, `opds_custom.scss` for styling
- `public/`: Generated static site output
- `meta/`: Job logs and metadata
- `output/`: Generated ebook files (local testing only)

## Recipe Scheduling
Use `_recipe_utils.py` helpers for conditional execution:
- `onlyat_hours([6,7,8], +5.5)`: Run only during specified hours in timezone
- `onlyon_weekdays()`: Monday-Friday only
- `onlyon_days([1,15])`: Specific days of month
- `first_n_days_of_month(7)`: First week only

## OPDS Integration
- Main catalog: `catalog.xml`
- Category catalogs: `{category-slug}.xml`
- Uses `_opds.py` for XML generation
- Styled with `static/opds.xsl` and `static/opds.scss`
- Content-type mapping in `extension_contenttype_map`

## Environment Variables
- `newsrack_title_dt_format`: Date format for titles (default: `%-d %b, %Y`)
- `recipes_includes`: Path to shared recipe components
- `CI_PAGES_URL`: Deployment URL for OPDS links

Always test recipes locally before committing. Use mechanize browser instead of webengine for better CI compatibility.
