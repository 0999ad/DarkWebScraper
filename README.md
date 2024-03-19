# TorScraperPro: Comprehensive Technical Overview

## Introduction

TorScraperPro is an advanced Python-based web scraping and content extraction tool. Designed for both privacy and efficiency, it navigates the web, including the Tor network, to extract content from specified websites based on user-defined keywords. Utilizing headless Chrome integrated with Selenium WebDriver, TorScraperPro effectively captures dynamic content. A Flask application dynamically serves the scraped HTML files, providing live updates and easy access to the data collected.

## Features

- **TOR Network Support**: Routes requests through the TOR network to ensure anonymity, enabling the scraping of .onion websites while maintaining user privacy.
- **Keyword-Based Scraping**: Focuses on extracting content that contains specified keywords, facilitating targeted data collection.
- **Dynamic Content Rendering**: With Selenium WebDriver, the tool can interact with JavaScript-heavy pages, ensuring comprehensive content capture.
- **Live Data Presentation**: A local Flask web server serves the scraped HTML files, offering a dashboard for live monitoring and access to scraped data.
- **Automatic ChromeDriver Management**: The script employs `webdriver_manager` to automatically select and use the correct ChromeDriver version, ensuring compatibility with the installed Google Chrome browser.
- **Flask Dashboard**: Provides a user-friendly interface for reviewing scraping outcomes, enhancing usability and accessibility.

## Dependencies

- Python 3.6 or later
- Flask
- Requests
- BeautifulSoup4
- Selenium WebDriver
- webdriver_manager
- Tor (Optional for .onion site scraping)

## Installation and Setup

1. **Install Python and Dependencies**:
    Ensure Python 3.6+ is installed on your system. Install the required Python packages using pip:

    ```bash
    pip install flask requests beautifulsoup4 selenium webdriver_manager
    ```

2. **Google Chrome**:
    Install the latest version of Google Chrome to ensure compatibility with ChromeDriver.

3. **TOR (Optional)**:
    For scraping .onion sites, install and configure TOR on your system.

4. **Clone the Repository**:
    Obtain the TorScraperPro script by cloning its repository to your local machine.

## Running Instructions

Execute TorScraperPro from the command line with the desired parameters:

```bash
python TorScraperPro.py -v -d <Depth> -p <Pause>
```

Options include:
- `-v`: Enables verbose logging for detailed operational insights.
- `-d <Depth>`: Defines the scraping depth for website traversal.
- `-p <Pause>`: Sets a pause duration between requests to mitigate server load and mimic human interaction.

## Key Functions

- **`setup_chrome()`**: Initializes a headless Chrome browser session for web interaction.
- **`check_tor_connection()`**: Verifies connectivity to the TOR network and logs the TOR-assigned IP address.
- **`get_keywords()`**: Loads keywords from a specified file, guiding the scraping focus.
- **`scrape_and_extract()`**: Core function that navigates to URLs, renders JavaScript, and extracts content based on keyword matches.
- **Flask Web Server**: Runs concurrently in a separate thread, serving scraped content through a user-friendly dashboard.

## Flask Web Server

Initiated at script startup, the Flask app presents a simple yet effective interface for real-time access to the scraped content. It facilitates navigation between current and archived runs, enhancing the review process of collected data.

## Conclusion

TorScraperPro version 1.0 emerges as a powerful solution for sophisticated web scraping needs, emphasizing privacy through TOR integration and flexibility with dynamic content handling. Its user-friendly dashboard and targeted scraping capabilities make it an invaluable tool for data analysts, researchers, and cybersecurity professionals.
