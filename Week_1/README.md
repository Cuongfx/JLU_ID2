# JLU_ID2
# Link Checker Documentation

## Overview

The Link Checker is a Python tool designed to scan web pages for HTTP links and verify their functionality by checking their HTTP status codes. This tool is particularly useful for website maintenance, ensuring that all external links on your website are working properly.

## For Users

### Basic Usage

The simplest way to use the Link Checker is through the command line:

```bash
python link-checker.py
```

When run without arguments, the tool will check the following default URLs:
- https://www.uni-giessen.de/ub/de/forlehr/fdm/wissenswertes/allgemein
- https://www.uni-giessen.de/ub/de/forlehr/fdm/wissenswertes/personenbezogene-daten

The results will be saved to a file named `links.md` in the current directory.

### Custom URLs and Output File

You can specify your own URLs and output file:

```bash
python link-checker.py https://example.com https://another-example.com results.md
```

The tool will automatically distinguish URLs from the output filename. The output filename should be the last argument.

### Getting Help

To display help information:

```bash
python link-checker.py --help
```

or

```bash
python link-checker.py -h
```

### Understanding the Results

The results are saved in a markdown file with a table containing:
1. **Source URL** - The original URL being checked
2. **Link** - Each HTTP link found on the page
3. **Status Code** - The HTTP status code for each link

Common HTTP status codes:
- **200** - OK (link is working)
- **301/302** - Redirect
- **403** - Forbidden
- **404** - Not Found (broken link)
- **500** - Internal Server Error
- **0** - Connection failed or timed out

## For Developers

### Module Overview

The `link-checker.py` module provides three main functions:

1. `get_link_status(link: str) -> tuple`
2. `extract_http_links(urls: list) -> dict`
3. `save_links_to_markdown(urls: list, filename: str)`

Additionally, it includes a `main()` function to enable command-line usage.

### Function Details

#### `get_link_status(link: str) -> tuple`

**Purpose**: Checks a single URL and returns its HTTP status code.

**Parameters**:
- `link` (str): The URL to check

**Returns**:
- A tuple `(link, status_code)` where:
  - `link` is the original URL
  - `status_code` is the HTTP status code (integer)

**Error Handling**:
- If the request fails (connection error, timeout, etc.), returns a status code of `0`

**Example**:
```python
from link_checker import get_link_status

status = get_link_status("https://www.example.com")
print(status)  # Output: ('https://www.example.com', 200)
```

#### `extract_http_links(urls: list) -> dict`

**Purpose**: Scans multiple web pages for links that start with "http" and checks their status.

**Parameters**:
- `urls` (list): A list of URLs to scan

**Returns**:
- A dictionary where:
  - Keys are the original URLs
  - Values are lists of tuples `(link, status_code)` for each link found

**Error Handling**:
- If a source URL is unreachable, its value in the dictionary will be an empty list

**Example**:
```python
from link_checker import extract_http_links

urls = ["https://www.example.com"]
result = extract_http_links(urls)
print(result)
# Output: {'https://www.example.com': [('https://api.example.com', 200), ('https://blog.example.com', 301)]}
```

#### `save_links_to_markdown(urls: list, filename: str)`

**Purpose**: Processes URLs and saves the results to a markdown file.

**Parameters**:
- `urls` (list): A list of URLs to scan
- `filename` (str): Path and filename for the output markdown file

**Returns**:
- None (writes results to a file)

**Error Handling**:
- Creates directories in the path if they don't exist
- Handles URLs that can't be reached

**Example**:
```python
from link_checker import save_links_to_markdown

urls = ["https://www.example.com"]
save_links_to_markdown(urls, "results/links.md")
# Creates results/links.md with a table of links and status codes
```

### Dependencies

The module depends on the following Python libraries:
- `requests` - For making HTTP requests
- `bs4` (Beautiful Soup 4) - For HTML parsing
- `re` - For regular expressions (though not extensively used in the current implementation)
- `os` - For file and directory operations

### Technical Limitations

1. **Performance**:
   - Each link check requires a separate HTTP request, which can be slow for pages with many links
   - No parallelization is implemented; links are checked sequentially

2. **Link Detection**:
   - Only detects links in `<a href>` tags
   - Only processes links that explicitly start with "http"
   - Does not handle relative links

3. **Error Handling**:
   - Request timeouts are set to 10 seconds
   - Failed requests are given a status code of 0
   - No retry mechanism for temporarily unavailable sites

4. **Memory Usage**:
   - For very large websites, the dictionary of results could consume significant memory

### Integration Examples

#### Using as a Module

```python
from link_checker import extract_http_links, save_links_to_markdown

# Get all links and their status
my_websites = ["https://mysite.com", "https://myothersite.com"]
results = extract_http_links(my_websites)

# Process the results programmatically
for site, links in results.items():
    print(f"Site: {site} has {len(links)} external links")
    broken_links = [link for link, status in links if status in [0, 404, 500]]
    if broken_links:
        print(f"  Warning: Found {len(broken_links)} broken links!")

# Save to markdown
save_links_to_markdown(my_websites, "weekly_link_report.md")
```

#### Extending the Functionality

To add support for JavaScript-rendered pages:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_links_with_javascript(url):
    # Set up headless browser
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    # Load the page
    driver.get(url)
    
    # Extract links
    links = []
    elements = driver.find_elements_by_tag_name('a')
    for element in elements:
        href = element.get_attribute('href')
        if href and href.startswith('http'):
            links.append(href)
    
    driver.quit()
    return links

# Then use this function in place of or alongside the BeautifulSoup implementation
```

## Contributing

Feel free to extend this tool with additional features, such as:

1. Parallel processing for faster link checking
2. Support for relative links
3. Link checking behind authentication
4. Recursive checking (following links to specified depth)
5. Custom HTTP headers for requests
6. Filtering links by domain
