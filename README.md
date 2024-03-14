# Extended DWScraper v1.3 Technical Overview

## Introduction

Extended DWScraper is a sophisticated Python-based web scraping tool designed to extract content from a predefined list of websites, including those hosted on the Tor network (.onion sites). It automatically checks each site for specified keywords and conditionally extracts content based on keyword matches. The tool supports extended timeouts for .onion sites and serves the scraped HTML files locally via a Flask application for live updates.

## Features

- **TOR Network Support**: The scraper can route requests through the TOR network, ensuring privacy and the ability to scrape .onion websites.
- **Keyword-Based Scraping**: Only extracts and saves content from websites containing specified keywords, allowing for targeted data collection.
- **Selenium Integration**: Utilizes Selenium WebDriver to handle JavaScript-heavy websites, ensuring dynamic content is rendered and captured.
- **Flask Web Server**: Dynamically serves the scraped HTML files through a local Flask web server, enabling live updates and easy access to scraped data.
- **Automatic ChromeDriver Management**: Leveraging `webdriver_manager`, the script automatically downloads and uses the correct ChromeDriver version based on the installed Google Chrome browser.

## Dependencies

- Python 3.6+
- Flask
- Requests
- BeautifulSoup4
- Selenium WebDriver
- WebDriver_Manager
- TOR (Optional for .onion sites)

## Installation and Setup

1. **Python and Dependencies**: Ensure Python 3.6+ is installed. Install all required Python packages using pip:

    ```bash
    pip install flask requests beautifulsoup4 selenium webdriver_manager
    ```

2. **Google Chrome**: Install the latest version of Google Chrome.

3. **TOR (Optional)**: Install and configure TOR if you plan to scrape .onion sites.

4. **Clone the Repository**: Clone the Extended DWScraper repository to your local machine.

## Usage

Run the script from the command line, specifying the desired options:

```bash
python extended_dwscraper.py -v -d <Depth> -p <Pause> -f <Output Folder Prefix>
```

- `-v`: Enable verbose logging.
- `-d <Depth>`: Set the scraping depth (integer).
- `-p <Pause>`: Set the pause duration between requests (seconds).
- `-f <Output Folder Prefix>`: Specify the prefix for the output directory where scraped content will be stored.

## Key Functions

- **`setup_tor_proxy()`**: Configures HTTP and HTTPS proxies for routing requests through the TOR network.
- **`check_tor(verbose=False)`**: Verifies connectivity to the TOR network and logs the TOR IP address.
- **`load_keywords(filepath='keywords.txt')`**: Loads keywords from a specified file. These keywords are used to filter which sites to scrape based on content matches.
- **`site_contains_keywords(url, keywords, proxies)`**: Checks if a given site contains any of the specified keywords.
- **`folder(name, verbose=False)`**: Creates a directory for storing scraped content.
- **`scrape_and_extract(url, depth, pause, out_path, proxies, verbose=False, keyword_str="")`**: Main scraping function. Utilizes Selenium WebDriver to navigate to a URL, render JavaScript if necessary, and extract content based on keyword matches.
- **`get_sites_from_markdown()`**: Fetches a list of sites to scrape from a predefined markdown file hosted on GitHub.
- **Flask App Routes**: Defines routes for serving the scraped HTML files through a local web server.

## Flask Web Server

The Flask application starts in a separate thread, ensuring it begins serving immediately upon script execution. It provides a simple interface for accessing scraped content stored as HTML files within the specified directory.

## Conclusion

Extended DWScraper v1.3 is a powerful tool for privacy-conscious, keyword-targeted web scraping, especially useful for dynamic content and .onion sites. Its integration with Selenium and Flask makes it a versatile solution for various scraping and content serving needs.
