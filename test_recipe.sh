#!/bin/bash
# filepath: /workspaces/newsrack/test_recipe.sh

# Test script for running Calibre recipe conversion
# Handles .recipe.py files and converts them to .epub format

# Set default values
OUTPUT_DIR="./output"
RECIPE_PATH=""
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -r, --recipe PATH     Specify recipe file path (.recipe.py)"
    echo "  -o, --output DIR      Specify output directory (default: ./output)"
    echo "  -v, --verbose         Enable verbose output"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -r recipes_custom/daily-current.recipe.py"
    echo "  $0 -r ./recipes/newsletters.recipe.py"
    echo "  $0 -r /full/path/to/recipe.recipe.py -o ./my_output"
    echo "  $0 -r recipes_custom/daily-current.recipe.py -v"
}

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--recipe)
            RECIPE_PATH="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Check if recipe path is provided
if [[ -z "$RECIPE_PATH" ]]; then
    print_status $RED "Error: Recipe file path must be specified with -r option"
    usage
    exit 1
fi

# Check if recipe file exists
if [[ ! -f "$RECIPE_PATH" ]]; then
    print_status $RED "Error: Recipe file '$RECIPE_PATH' not found"
    exit 1
fi

# Extract filename from path and check if it's a .recipe.py file
RECIPE_FILE=$(basename "$RECIPE_PATH")
if [[ ! "$RECIPE_FILE" =~ \.recipe\.py$ ]]; then
    print_status $RED "Error: Recipe file must have .recipe.py extension"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Generate output filename (remove .recipe.py and add .epub)
RECIPE_NAME=$(basename "$RECIPE_FILE" .recipe.py)
OUTPUT_FILE="$OUTPUT_DIR/${RECIPE_NAME}_$(date +%Y%m%d_%H%M%S).epub"

# Create temporary .recipe file by copying the .recipe.py file
TEMP_RECIPE="/tmp/${RECIPE_NAME}.recipe"
cp "$RECIPE_PATH" "$TEMP_RECIPE"

print_status $GREEN "Starting recipe conversion..."
print_status $YELLOW "Recipe: $RECIPE_PATH"
print_status $YELLOW "Temp recipe: $TEMP_RECIPE"
print_status $YELLOW "Output: $OUTPUT_FILE"

# Build ebook-convert command using the temporary .recipe file
CONVERT_CMD="ebook-convert \"$TEMP_RECIPE\" \"$OUTPUT_FILE\" -vvv --debug-pipeline debug"

# Add verbose flag if requested
if [[ "$VERBOSE" == true ]]; then
    CONVERT_CMD="$CONVERT_CMD --verbose"
fi

print_status $GREEN "Running command: $CONVERT_CMD"

# Execute the conversion
if eval $CONVERT_CMD; then
    print_status $GREEN "✓ Conversion completed successfully!"
    print_status $GREEN "✓ Output file: $OUTPUT_FILE"
    
    # Display file size
    if [[ -f "$OUTPUT_FILE" ]]; then
        FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
        print_status $GREEN "✓ File size: $FILE_SIZE"
    fi
    
    # Clean up temporary file
    rm -f "$TEMP_RECIPE"
    
else
    print_status $RED "✗ Conversion failed!"
    # Clean up temporary file even on failure
    rm -f "$TEMP_RECIPE"
    exit 1
fi
