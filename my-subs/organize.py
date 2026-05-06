#!/usr/bin/env python3
"""Organize SRT subtitle files into TXT format with season/episode structure"""

import os
import re
import glob

INPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(INPUT_DIR, "my_subtitles")

def parse_srt(content):
    """Parse SRT content and extract dialogue text"""
    lines = content.split('\n')
    dialogue_lines = []
    skip_header = True

    for line in lines:
        line = line.strip()

        # Skip empty lines and SRT formatting
        if not line:
            continue

        # Skip timestamp lines
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}', line):
            continue

        # Skip sequence numbers
        if re.match(r'^\d+$', line):
            continue

        # Skip header/intro lines
        if skip_header:
            if 'WWW.MY-SUBS.COM' in line or 'Translated By' in line or 'Synced & corrected' in line:
                continue
            if '<font' in line.lower():
                continue
            skip_header = False

        # Remove HTML tags
        clean_line = re.sub(r'<[^>]+>', '', line)

        # Skip empty lines after cleaning
        if clean_line.strip():
            dialogue_lines.append(clean_line.strip())

    return '\n'.join(dialogue_lines)

def parse_episode_filename(filename):
    """Parse SXXEXX from filename"""
    match = re.match(r'S(\d+)E(\d+)\.srt', filename, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def get_episode_title(filepath):
    """Extract episode title from SRT content (usually in first few lines)"""
    try:
        with open(filepath, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read(500)  # Read first 500 chars
    except:
        return "Episode"

    # Try to find episode title in comments or first dialogue
    lines = content.split('\n')
    for line in lines[:10]:
        line = line.strip()
        if line and not re.match(r'^\d+$', line) and not re.match(r'\d{2}:\d{2}:\d{2}', line):
            if 'WWW.MY-SUBS.COM' not in line and 'Translated' not in line:
                # Remove HTML tags
                clean_line = re.sub(r'<[^>]+>', '', line)
                if clean_line.strip():
                    return clean_line.strip()[:50]  # Return first 50 chars as title
    return "Episode"

def main():
    print("Organizing SRT files into TXT format...")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find all SRT files
    srt_files = glob.glob(os.path.join(INPUT_DIR, "S*.srt"))
    print(f"Found {len(srt_files)} SRT files")

    organized = 0
    failed = 0

    for srt_path in sorted(srt_files):
        filename = os.path.basename(srt_path)
        season, episode = parse_episode_filename(filename)

        if not season or not episode:
            print(f"Skipping {filename} - cannot parse episode info")
            failed += 1
            continue

        # Create season directory
        season_dir = os.path.join(OUTPUT_DIR, f"Season_{season}")
        os.makedirs(season_dir, exist_ok=True)

        # Read and parse SRT content
        try:
            with open(srt_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()

            dialogue = parse_srt(content)
            title = get_episode_title(srt_path)

            # Create output filename
            txt_filename = f"S{season:02d}E{episode:02d}.txt"
            txt_path = os.path.join(season_dir, txt_filename)

            # Write TXT file
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: The Middle S{season:02d}E{episode:02d} - {title}\n")
                f.write(f"Source: my-subs.co\n")
                f.write(f"File: {filename}\n\n")
                f.write(dialogue)

            print(f"  S{season:02d}E{episode:02d} -> {txt_filename}")
            organized += 1

        except Exception as e:
            print(f"  Error processing {filename}: {e}")
            failed += 1

    print(f"\nDone! Organized: {organized}, Failed: {failed}")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
