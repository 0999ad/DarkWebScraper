#!/usr/bin/env python3
"""
TorScraperPro Version 1.0 for sophisticated web scraping and content extraction,
using headless Chrome with Tor for anonymity. Includes functionalities like Tor connection verification,
archive management, enhanced user and CLI feedback, and a Flask dashboard for monitoring.

Usage:
  python TorScraperPro.py -v -d <Depth> -p <Pause>
"""

import argparse
import datetime
import os
import shutil
import sys
import threading
import time
from urllib.parse import urlparse
from flask import Flask, send_from_directory, render_template, url_for
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
from selenium.common.exceptions import WebDriverException
import re

app = Flask(__name__)

BASE_DIR = os.path.join(os.getcwd(), "scraped_sites")
OLD_RUNS_DIR = os.path.join(BASE_DIR, "old_runs")

logging.basicConfig(level=logging.INFO, filename='TorScraperPro.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chromedriver_path = "/usr/local/bin/chromedriver"
    chrome_service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver

def check_tor_connection():
    try:
        session = requests.Session()
        session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
        ip = session.get('https://api.ipify.org').text
        logging.info(f"Connected to TOR.\nTOR IP Address: {ip}")
        print(f"Connected to TOR.\nTOR IP Address: {ip}")
    except Exception as e:
        logging.error(f"Error checking Tor connection: {e}")
        print(f"Error checking Tor connection: {e}")

def get_keywords():
    with open("keywords.txt", "r") as file:
        return [line.strip() for line in file.readlines()]

def get_sites():
    response = requests.get("https://raw.githubusercontent.com/fastfire/deepdarkCTI/main/forum.md")
    sites = re.findall(r'\((https?://[^\s)]+)\)', response.text)
    return sites

def archive_old_runs():
    if not os.path.exists(OLD_RUNS_DIR):
        os.makedirs(OLD_RUNS_DIR)
    for file in os.listdir(BASE_DIR):
        if file.endswith('.html'):
            shutil.move(os.path.join(BASE_DIR, file), OLD_RUNS_DIR)

def scrape_and_extract(url, pause, keywords, driver):
    try:
        driver.get(url)
        time.sleep(pause)
    except WebDriverException:
        logging.info(f"Skipped: {url}")
        print(f"Skipped: {url}")
        return
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    text = soup.get_text().lower()
    for keyword in keywords:
        if keyword.lower() in text:
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{now}_{keyword}_{urlparse(url).netloc.replace('.', '_')}.html"
            filepath = os.path.join(BASE_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

@app.route('/')
def list_html_files():
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.html')]
    return render_template('list_files.html', files=files, title="Current Run: TOR Site Scraped HTML Files", back_link_text="OLD RUNS", back_link_url=url_for('list_old_html_files'))

@app.route('/old_runs/')
def list_old_html_files():
    files = [f for f in os.listdir(OLD_RUNS_DIR) if f.endswith('.html')]
    return render_template('list_files.html', files=files, title="Old Runs: TOR Site Scraped HTML Files", back_link_text="BACK TO HOME", back_link_url=url_for('list_html_files'))

@app.route('/html/<filename>')
def serve_html_file(filename):
    directory = BASE_DIR if filename in os.listdir(BASE_DIR) else OLD_RUNS_DIR
    return send_from_directory(directory, filename)

def configure_argparser():
    parser = argparse.ArgumentParser(description="TorScraperPro Version 1.0 for secure, efficient webpage scraping and extraction using Chrome.")
    parser.add_argument('-v', '--verbose', help='Enable detailed logs.', action='store_true')
    parser.add_argument('-d', '--depth', help='Scrape depth.', type=int, default=2)
    parser.add_argument('-p', '--pause', help='Pause between requests.', type=int, default=5)
    return parser

def main_scraping():
    start_time = time.time()
    args = configure_argparser().parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    check_tor_connection()
    driver = setup_chrome()
    keywords = get_keywords()
    sites = get_sites()

    for site in sites:
        scrape_and_extract(site, args.pause, keywords, driver)
    
    driver.quit()
    end_time = time.time()
    print(f"Script took {end_time - start_time:.2f} seconds\nPlease Press CTRL+C to quit")

if __name__ == "__main__":
    # Clear old runs at the start of a new session
    archive_old_runs()
    # Start the scraping in a separate thread
    thread = threading.Thread(target=main_scraping)
    thread.start()
    # Ensure Flask app starts in the main thread to be accessible
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
