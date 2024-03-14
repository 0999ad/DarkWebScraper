#!/usr/bin/env python3
"""
Extended DWScraper (v1.3) for sophisticated web scraping and content extraction via TOR,
ensuring privacy. Automatically scrapes from a predefined list of sites, checks for specified
keywords, and conditionally extracts content. Supports .onion sites with extended timeouts and
serves scraped HTML files locally via Flask for live updates.

Usage:
  python extended_dwscraper.py -v -d <Depth> -p <Pause> -f <Output Folder Prefix>
"""

import argparse
import datetime
import json
import os
import re
import sys
import time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, send_from_directory
from werkzeug.utils import safe_join

app = Flask(__name__)
HTML_DIR = 'scraped_sites'  # Directory where HTML files are stored

# Initialize logging
logging.basicConfig(filename='extended_dwscraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hardcoded URL of the markdown file containing the list of sites to scrape
SITE_LIST_URL = "https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/forum.md"

def setup_tor_proxy():
    return {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}

def check_tor(verbose=False):
    proxies = setup_tor_proxy()
    try:
        response = requests.get('https://check.torproject.org/api/ip', proxies=proxies)
        if verbose:
            print(f"TOR IP: {response.json().get('IP')}")
        print("Successfully connected to TOR.")
    except RequestException as e:
        print(f"Error checking TOR connection: {e}")
        sys.exit(1)

def load_keywords(filepath='keywords.txt'):
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"Keywords file {filepath} not found.")
        return []

def site_contains_keywords(url, keywords, proxies):
    matched_keywords = []
    timeout = 30 if url.endswith(".onion") else 10
    try:
        response = requests.get(url, proxies=proxies, timeout=timeout)
        page_content = response.text.lower()
        for keyword in keywords:
            if keyword.lower() in page_content:
                matched_keywords.append(keyword)
        return matched_keywords
    except Timeout:
        logging.error(f"{urlparse(url).netloc} TOR timeout, skipping to next site.")
        return []
    except RequestException as e:
        logging.error(f"Failed to fetch or process site content: {url}, Error: {e}")
        return []

def folder(name, verbose=False):
    path = os.path.join(os.getcwd(), name)
    os.makedirs(path, exist_ok=True)
    if verbose:
        print(f"Setting up folder: {path}")
    return path

def scrape_and_extract(url, depth, pause, out_path, proxies, verbose=False, keyword_str=""):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:9050')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    time.sleep(pause)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    title = soup.title.text if soup.title else 'No Title'
    all_text = ' '.join(soup.stripped_strings)

    data = {'url': url, 'title': title, 'text': all_text}
    with open(os.path.join(out_path, f"{title}.json"), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
    with open(os.path.join(out_path, f"{title}.html"), 'w', encoding='utf-8') as html_file:
        html_file.write(soup.prettify())

    if verbose:
        print(f"Saved: {os.path.join(out_path, f'{title}.json')}")
        print(f"Saved: {os.path.join(out_path, f'{title}.html')}")

    driver.quit()

def get_sites_from_markdown():
    try:
        response = requests.get(SITE_LIST_URL)
        response.raise_for_status()
        links = re.findall(r'\[(.*?)\]\((http[s]?://.*?)\)', response.text)
        return [link[1] for link in links if not link[1].endswith('.onion')]
    except RequestException as e:
        logging.error(f"Failed to fetch site list: {e}")
        return []

@app.route('/')
def list_html_files():
    files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
    links = [f'<li><a href="/html/{f}">{f}</a></li>' for f in files]
    return f'<ul>{" ".join(links)}</ul>'

@app.route('/html/<path:filename>')
def serve_html_file(filename):
    safe_path = safe_join(HTML_DIR, filename)
    if not os.path.exists(safe_path):
        return "File not found.", 404
    return send_from_directory(HTML_DIR, filename)

def configure_argparser():
    parser = argparse.ArgumentParser(description="Extended DWScraper for secure, efficient webpage scraping and extraction.")
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable detailed logs.')
    parser.add_argument('-d', '--sdepth', type=int, default=1, help='Scrape depth.')
    parser.add_argument('-p', '--pause', type=int, default=5, help='Pause between requests.')
    parser.add_argument('-f', '--folder', required=True, help='Output directory prefix for extracted content.')
    return parser

def main():
    parser = configure_argparser()
    args = parser.parse_args()

    if not os.path.exists(HTML_DIR):
        os.makedirs(HTML_DIR)

    keywords = load_keywords()
    proxies = setup_tor_proxy()
    check_tor(verbose=args.verbose)
    sites = get_sites_from_markdown()

    for site in sites:
        matched_keywords = site_contains_keywords(site, keywords, proxies)
        if matched_keywords:
            keyword_str = "_".join(matched_keywords)
            print(f"Keyword(s) '{', '.join(matched_keywords)}' found in {site}")
            site_netloc = urlparse(site).netloc
            out_path = folder(f"{args.folder}_{site_netloc}_{keyword_str}_Found", verbose=args.verbose)
            scrape_and_extract(site, args.sdepth, args.pause, out_path, proxies, args.verbose, keyword_str)
        else:
            print(f"No keywords found in {site}. Skipping scrape.")

if __name__ == "__main__":
    # Start Flask app in a separate thread to ensure it starts serving immediately
    flask_thread = threading.Thread(target=lambda: app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False), daemon=True)
    flask_thread.start()

    main()
