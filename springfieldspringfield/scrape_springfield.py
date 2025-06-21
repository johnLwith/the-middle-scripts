import requests
from bs4 import BeautifulSoup
import os
import time
import re

def create_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_filename(filename):
    """Clean filename by removing illegal characters"""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def extract_episode_info(episode_link):
    """Extract season and episode numbers from episode link"""
    # Example: view_episode_scripts.php?tv-show=the-middle&episode=s01e01
    pattern = r'episode=s(\d+)e(\d+)'
    match = re.search(pattern, episode_link)
    if match:
        season_num = int(match.group(1))
        episode_num = int(match.group(2))
        return season_num, episode_num
    return None, None

def scrape_episode_script(episode_url):
    """Scrape script content from an individual episode page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(episode_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get episode title from page title
        title_element = soup.find('title')
        if title_element:
            title = title_element.text.strip()
            # Extract just the episode part from "The Middle s01e01 Episode Script | SS"
            title = title.replace(' Episode Script | SS', '').replace('The Middle ', '')
        else:
            title = "Unknown Episode"
        
        # Get script content from the scrolling container
        script_container = soup.find('div', class_='scrolling-script-container')
        if script_container:
            # Get all text content and clean it up
            script_content = script_container.get_text(separator='\n', strip=True)
            # Remove excessive line breaks
            script_content = re.sub(r'\n\s*\n', '\n\n', script_content)
        else:
            script_content = "Script content not found."
        
        return title, script_content
    except Exception as e:
        print(f"Error scraping episode {episode_url}: {e}")
        return None, None

def scrape_all_episodes(main_url):
    """Scrape all episode information from the main page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Accessing main page: {main_url}")
        response = requests.get(main_url, headers=headers)
        response.raise_for_status()
        
        print(f"Page status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Print page title
        title = soup.find('title')
        if title:
            print(f"Page title: {title.text}")
        
        # Find all episode links
        episodes_by_season = {}
        
        # Look for episode links in the format: view_episode_scripts.php?tv-show=the-middle&episode=s01e01
        episode_links = soup.find_all('a', href=re.compile(r'view_episode_scripts\.php\?tv-show=the-middle&episode=s\d+e\d+'))
        
        print(f"Found {len(episode_links)} episode links")
        
        for link in episode_links:
            href = link['href']
            episode_url = 'https://www.springfieldspringfield.co.uk/' + href
            season_num, episode_num = extract_episode_info(href)
            
            if season_num is not None:
                if season_num not in episodes_by_season:
                    episodes_by_season[season_num] = []
                
                episodes_by_season[season_num].append({
                    'url': episode_url,
                    'title': link.text.strip(),
                    'episode_num': episode_num
                })
        
        # Print number of seasons found
        print(f"Found {len(episodes_by_season)} seasons")
        
        # Sort episodes by episode number for each season
        for season_num in episodes_by_season:
            episodes_by_season[season_num].sort(key=lambda x: x['episode_num'])
            print(f"Season {season_num}: {len(episodes_by_season[season_num])} episodes")
        
        return episodes_by_season
    except Exception as e:
        print(f"Error scraping main page {main_url}: {e}")
        import traceback
        print("Detailed error information:")
        print(traceback.format_exc())
        return {}

def main():
    """Main function"""
    main_url = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-middle"
    output_dir = "springfield_scripts"

    print(f"Starting to scrape 'The Middle' episode scripts from Springfield Springfield...")

    # Create output directory
    create_directory(output_dir)

    # Scrape all episode information
    episodes_by_season = scrape_all_episodes(main_url)

    if not episodes_by_season:
        print("No episodes found. Exiting.")
        return

    # Check if this is a test run (limit to first few episodes)
    import sys
    test_mode = '--test' in sys.argv
    if test_mode:
        print("Running in test mode - limiting to first 3 episodes of Season 1")

    # Iterate through each season
    for season_num in sorted(episodes_by_season.keys()):
        season_dir = os.path.join(output_dir, f"Season_{season_num}")
        create_directory(season_dir)

        print(f"Scraping Season {season_num}...")

        # Iterate through each episode in the season
        episodes_to_process = episodes_by_season[season_num]
        if test_mode and season_num == 1:
            episodes_to_process = episodes_to_process[:3]  # Limit to first 3 episodes
        elif test_mode and season_num > 1:
            continue  # Skip other seasons in test mode

        for episode_info in episodes_to_process:
            print(f"  Scraping Season {season_num} Episode {episode_info['episode_num']}: {episode_info['title']}...")

            # Scrape script content
            title, script_content = scrape_episode_script(episode_info['url'])

            if title and script_content:
                # Save script content to file
                clean_title = clean_filename(title)
                filename = os.path.join(season_dir, f"{episode_info['episode_num']:02d}_{clean_title}.txt")

                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"Title: {title}\n")
                    file.write(f"URL: {episode_info['url']}\n\n")
                    file.write(script_content)

                print(f"    Saved: {filename}")
            else:
                print(f"    Failed to scrape: {episode_info['url']}")

            # Add delay to avoid too frequent requests
            time.sleep(1)

    if test_mode:
        print("Test run completed!")
    else:
        print("Scraping completed!")

if __name__ == "__main__":
    main()
