#!/usr/bin/env python3
"""Scrape English subtitles from my-subs.co for The Middle"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://my-subs.co"
SHOW_URL = f"{BASE_URL}/showlistsubtitles-1702-the-middle"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_episode_links():
    """Get all episode links from the show page"""
    resp = requests.get(SHOW_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/versions-' in href and 'the-middle-subtitles' in href:
            links.append(href)
    return links

def get_english_download_gate_url(episode_url):
    """Get the English subtitle gate URL from an episode page"""
    resp = requests.get(f"{BASE_URL}{episode_url}", headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Find all subtitle entries
    rows = soup.find_all('div', class_='row')

    for row in rows:
        # Check if it's English - look at both the lang div and span
        lang_div = row.find('div', class_='lang')
        if lang_div:
            # Check span title or text content
            span = lang_div.find('span')
            if span and 'english' in span.get('title', '').lower():
                download_link = row.find('a', href=re.compile(r'/downloads/'))
                if download_link:
                    return download_link['href']
            # Also check the <i> tag text
            i_tag = lang_div.find('i')
            if i_tag and 'english' in i_tag.text.lower():
                download_link = row.find('a', href=re.compile(r'/downloads/'))
                if download_link:
                    return download_link['href']

    return None

def get_real_download_url(gate_url, session):
    """Get the real download URL from the gate page"""
    resp = session.get(f"{BASE_URL}{gate_url}")
    # Extract REAL_URL from JavaScript (remove escaped backslash)
    match = re.search(r'var REAL_URL="([^"]+)"', resp.text)
    if match:
        return match.group(1).replace('\\/', '/')
    return None

def download_subtitle(real_url, gate_url, session):
    """Download a subtitle file using the real URL"""
    resp = session.get(
        f"{BASE_URL}{real_url}",
        headers={**HEADERS, 'Referer': f"{BASE_URL}{gate_url}"},
        allow_redirects=True
    )
    return resp.content

def parse_episode_info(episode_url):
    """Parse season and episode number from URL"""
    match = re.search(r'/versions-1702-(\d+)-(\d+)-the-middle-subtitles', episode_url)
    if match:
        episode = match.group(1)
        season = match.group(2)
        return int(season), int(episode)
    return None, None

def main():
    print("Fetching episode links...")
    episode_links = get_episode_links()
    print(f"Found {len(episode_links)} episodes")

    # Create directory structure
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    downloaded = 0
    failed = 0

    for i, link in enumerate(episode_links):
        season, episode = parse_episode_info(link)
        if not season or not episode:
            print(f"Could not parse: {link}")
            failed += 1
            continue

        print(f"[{i+1}/{len(episode_links)}] Season {season} Episode {episode}...", end=" ")

        try:
            # Create a new session for each episode
            session = requests.Session()
            session.headers.update(HEADERS)

            # Get gate URL from episode page
            gate_url = get_english_download_gate_url(link)
            if not gate_url:
                print("No download link found")
                failed += 1
                continue

            # Get real download URL from gate page
            real_url = get_real_download_url(gate_url, session)
            if not real_url:
                print("Could not get real URL")
                failed += 1
                continue

            # Download the file
            content = download_subtitle(real_url, gate_url, session)

            # Validate it's an SRT file (starts with numbers or has SRT structure)
            content_str = content.decode('utf-8', errors='ignore')[:100]
            if '<html' in content_str.lower() or '<!doctype' in content_str.lower():
                print("Failed - got HTML instead of SRT")
                failed += 1
                continue

            # Save the file
            filename = f"S{season:02d}E{episode:02d}.srt"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(content)
            print(f"OK ({len(content)} bytes)")
            downloaded += 1

        except Exception as e:
            print(f"Error: {e}")
            failed += 1

        # Be polite to the server
        time.sleep(1)

    print(f"\nDone! Downloaded: {downloaded}, Failed: {failed}")

if __name__ == "__main__":
    main()
