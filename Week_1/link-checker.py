import requests
from bs4 import BeautifulSoup
import re
import os

def get_link_status(link: str) -> tuple:
    '''
    Takes a link as a string and returns a tuple containing the link and the http status code.
    
    Args:
        link (str): The URL to check
        
    Returns:
        tuple: A tuple containing the link and its HTTP status code
    '''
    try:
        response = requests.get(link, timeout=10)
        status_code = response.status_code
    except requests.exceptions.RequestException:
        status_code = 0  # Error code for failed requests
        
    return (link, status_code)

def extract_http_links(urls: list) -> dict:
    '''
    Takes a list of URLs and returns a dictionary with each URL as a key and a list of tuples 
    of all contained links starting with "http" and their http status codes as a value.
    
    Args:
        urls (list): List of URLs to scan for links
        
    Returns:
        dict: Dictionary with URLs as keys and lists of (link, status_code) tuples as values
    '''
    result = {}
    
    for url in urls:
        try:
            # Get the page content
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all links
            links = []
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                # Only process links starting with http
                if href.startswith('http'):
                    links.append(href)
            
            # Get status for each link
            status_links = []
            for link in links:
                status_links.append(get_link_status(link))
                
            # Add to result
            result[url] = status_links
            
        except requests.exceptions.RequestException:
            # If the URL itself is unreachable, add an empty list
            result[url] = []
            
    return result

def save_links_to_markdown(urls: list, filename: str):
    '''
    Takes a list of URLs and outputs a Markdown file (.md) containing a table with the URLs 
    and the links they contain with their http status codes.
    
    Args:
        urls (list): List of URLs to scan for links
        filename (str): Path and filename for the output markdown file
    '''
    # Get links and their status codes
    links_dict = extract_http_links(urls)
    
    # Create directory if needed and if there's a directory path
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    # Create markdown content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Link Checker Results\n\n")
        f.write("| Source URL | Link | Status Code |\n")
        f.write("|------------|------|------------|\n")
        
        for url in urls:
            links = links_dict.get(url, [])
            
            if links:
                # Add each link with its status code
                for link, status in links:
                    f.write(f"| {url} | {link} | {status} |\n")
            else:
                # If no links were found or the URL was unreachable
                f.write(f"| {url} | No links found or URL unreachable | - |\n")

def main():
    """
    Main function to allow command-line usage
    """
    import sys
    
    # Default URLs if none provided
    default_urls = [
        "https://www.uni-giessen.de/ub/de/forlehr/fdm/wissenswertes/allgemein",
        "https://www.uni-giessen.de/ub/de/forlehr/fdm/wissenswertes/personenbezogene-daten"
    ]
    
    # Default output path is simply the filename in the current directory
    default_output = "links.md"
    
    # Check for command-line arguments
    if len(sys.argv) > 1:
        # Check if help flag is provided
        if sys.argv[1] in ['-h', '--help']:
            print("Usage: python link-checker.py [url1 url2 ...] [output_file]")
            print("If no URLs are provided, default URLs will be used.")
            print("If no output file is provided, 'links.md' will be used.")
            sys.exit(0)
            
        # Get URLs from command-line
        urls = []
        output_file = default_output
        
        for arg in sys.argv[1:]:
            if arg.startswith('http'):
                urls.append(arg)
            else:
                output_file = arg
                
        if not urls:
            urls = default_urls
    else:
        urls = default_urls
        output_file = default_output
    
    # Run the link checker
    save_links_to_markdown(urls, output_file)
    print(f"Link check completed. Results saved to {output_file}")

# Use these URLs as specified in the assignment
urls = [
    "https://www.uni-giessen.de/ub/de/forlehr/fdm/wissenswertes/allgemein",
    "https://www.uni-giessen.de/ub/de/forlehr/fdm/wissenswertes/personenbezogene-daten"
]

# If this file is run directly, use the main function
if __name__ == "__main__":
    main()