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

def extract_episode_info(url):
    """Extract season and episode numbers from URL"""
    pattern = r'/season-(\d+)/episode-(\d+)'
    match = re.search(pattern, url)
    if match:
        season_num = int(match.group(1))
        episode_num = int(match.group(2))
        return season_num, episode_num
    return None, None

def scrape_episode_script(episode_url):
    """Scrape script content for a single episode"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(episode_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get episode title
        title_element = soup.find('h1')
        if title_element:
            title = title_element.text.strip()
        else:
            title = "Unknown Episode"
        
        # Get script content
        script_div = soup.find('div', class_='full-script')
        if script_div:
            script_content = script_div.get_text(strip=True, separator='\n')
        else:
            script_content = "Script content not found."
        
        return title, script_content
    except Exception as e:
        print(f"Error scraping episode {episode_url}: {e}")
        return None, None

def scrape_all_episodes(main_url):
    """Scrape all episode information directly from the main page"""
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
        episodes = []
        episode_elements = soup.select('.season a')
        print(f"Found {len(episode_elements)} episode links")
        
        # Organize episodes by season
        episodes_by_season = {}
        
        for element in episode_elements:
            href = element['href']
            episode_url = 'https://subslikescript.com' + href
            season_num, episode_num = extract_episode_info(href)
            
            if season_num is not None:
                if season_num not in episodes_by_season:
                    episodes_by_season[season_num] = []
                
                episodes_by_season[season_num].append({
                    'url': episode_url,
                    'title': element.text.strip(),
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
    main_url = "https://subslikescript.com/series/The_Middle-1442464"
    output_dir = "the_middle_scripts"
    
    print(f"Starting to scrape 'The Middle' episode scripts...")
    
    # Create output directory
    create_directory(output_dir)
    
    # Scrape all episode information directly
    episodes_by_season = scrape_all_episodes(main_url)
    
    # Iterate through each season
    for season_num in sorted(episodes_by_season.keys()):
        season_dir = os.path.join(output_dir, f"Season_{season_num}")
        create_directory(season_dir)
        
        print(f"Scraping Season {season_num}...")
        
        # Iterate through each episode in the season
        for episode_info in episodes_by_season[season_num]:
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
            
            # Add delay to avoid too frequent requests
            time.sleep(1)
    
    print("Scraping completed!")

if __name__ == "__main__":
    main()