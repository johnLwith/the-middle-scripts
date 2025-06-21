import os
import re
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Visualizations will be skipped.")

def count_words_in_file(file_path):
    """
    Count the number of words in a given text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The number of words in the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Skip metadata (title and source URL)
            lines = content.split('\n')[2:]
            text = '\n'.join(lines)
            words = re.findall(r'\w+', text.lower())
            return len(words)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return 0

def analyze_seasons(scripts_dir):
    """
    Analyze word count statistics for each season.

    Args:
        scripts_dir (str): The directory containing season subdirectories.

    Returns:
        dict: A dictionary with season statistics.
    """
    season_stats = {}
    
    for season_dir in sorted(os.listdir(scripts_dir)):
        season_path = os.path.join(scripts_dir, season_dir)
        if os.path.isdir(season_path) and season_dir.startswith('Season_'):
            season_num = int(season_dir.split('_')[1])
            
            episode_word_counts = []
            episode_count = 0
            
            for filename in sorted(os.listdir(season_path)):
                if filename.endswith('.txt'):
                    file_path = os.path.join(season_path, filename)
                    word_count = count_words_in_file(file_path)
                    episode_word_counts.append(word_count)
                    episode_count += 1
            
            if episode_word_counts:
                total_words = sum(episode_word_counts)
                avg_words = total_words / len(episode_word_counts)
                
                season_stats[season_num] = {
                    'total_words': total_words,
                    'avg_words_per_episode': avg_words,
                    'episode_counts': episode_count,
                    'word_counts': episode_word_counts
                }
    
    return season_stats

def analyze_character_dialogue(scripts_dir):
    """
    Analyze character dialogue patterns across all scripts.

    Args:
        scripts_dir (str): The directory containing season subdirectories.

    Returns:
        dict: Character dialogue statistics.
    """
    character_stats = defaultdict(int)
    
    # Common character patterns in The Middle scripts
    character_patterns = [
        r'FRANKIE:',
        r'MIKE:',
        r'SUE:',
        r'AXL:',
        r'BRICK:',
        r'NANCY:',
        r'RITA:',
        r'BRAD:',
        r'SEAN:',
        r'CINDY:'
    ]
    
    for season_dir in os.listdir(scripts_dir):
        season_path = os.path.join(scripts_dir, season_dir)
        if os.path.isdir(season_path) and season_dir.startswith('Season_'):
            for filename in os.listdir(season_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(season_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            
                            for pattern in character_patterns:
                                character_name = pattern.replace(':', '')
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                character_stats[character_name] += len(matches)
                    except Exception as e:
                        print(f"Error analyzing {file_path}: {e}")
    
    return dict(character_stats)

def plot_season_statistics(season_stats):
    """
    Create visualizations for season statistics.

    Args:
        season_stats (dict): Season statistics from analyze_seasons.
    """
    if not season_stats:
        print("No season statistics to plot.")
        return
    
    seasons = sorted(season_stats.keys())
    total_words = [season_stats[s]['total_words'] for s in seasons]
    avg_words = [season_stats[s]['avg_words_per_episode'] for s in seasons]
    episode_counts = [season_stats[s]['episode_counts'] for s in seasons]
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('The Middle Scripts Analysis - Springfield Springfield', fontsize=16)
    
    # Total words per season
    ax1.bar(seasons, total_words, color='skyblue')
    ax1.set_title('Total Words per Season')
    ax1.set_xlabel('Season')
    ax1.set_ylabel('Total Words')
    ax1.grid(True, alpha=0.3)
    
    # Average words per episode
    ax2.plot(seasons, avg_words, marker='o', color='orange', linewidth=2)
    ax2.set_title('Average Words per Episode by Season')
    ax2.set_xlabel('Season')
    ax2.set_ylabel('Average Words per Episode')
    ax2.grid(True, alpha=0.3)
    
    # Episode counts per season
    ax3.bar(seasons, episode_counts, color='lightgreen')
    ax3.set_title('Number of Episodes per Season')
    ax3.set_xlabel('Season')
    ax3.set_ylabel('Episode Count')
    ax3.grid(True, alpha=0.3)
    
    # Word count distribution (box plot)
    word_count_data = [season_stats[s]['word_counts'] for s in seasons]
    ax4.boxplot(word_count_data, labels=seasons)
    ax4.set_title('Word Count Distribution by Season')
    ax4.set_xlabel('Season')
    ax4.set_ylabel('Words per Episode')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'season_analysis.png'), dpi=300, bbox_inches='tight')
    plt.show()

def plot_character_dialogue(character_stats):
    """
    Create visualization for character dialogue statistics.

    Args:
        character_stats (dict): Character dialogue statistics.
    """
    if not character_stats:
        print("No character statistics to plot.")
        return
    
    # Sort characters by dialogue count
    sorted_characters = sorted(character_stats.items(), key=lambda x: x[1], reverse=True)
    characters = [item[0] for item in sorted_characters[:10]]  # Top 10 characters
    dialogue_counts = [item[1] for item in sorted_characters[:10]]
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(characters, dialogue_counts, color='lightcoral')
    plt.title('Character Dialogue Frequency - Springfield Springfield Scripts')
    plt.xlabel('Character')
    plt.ylabel('Number of Dialogue Lines')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, count in zip(bars, dialogue_counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(count), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(__file__), 'character_analysis.png'), dpi=300, bbox_inches='tight')
    plt.show()

def main():
    scripts_dir = 'springfield_scripts'
    if not os.path.exists(scripts_dir):
        print(f"Directory {scripts_dir} not found. Please run the scraping script first.")
        return

    print("Analyzing Springfield Springfield scripts...")
    
    # Analyze seasons
    season_stats = analyze_seasons(scripts_dir)
    print("\nSeason Statistics:")
    for season in sorted(season_stats.keys()):
        stats = season_stats[season]
        print(f"Season {season}:")
        print(f"  Total Words: {stats['total_words']:,}")
        print(f"  Average Words per Episode: {stats['avg_words_per_episode']:.2f}")
        print(f"  Episode Count: {stats['episode_counts']}")
    
    # Analyze character dialogue
    character_stats = analyze_character_dialogue(scripts_dir)
    print("\nTop Character Dialogue Counts:")
    sorted_characters = sorted(character_stats.items(), key=lambda x: x[1], reverse=True)
    for character, count in sorted_characters[:10]:
        print(f"  {character}: {count}")
    
    # Create visualizations
    if MATPLOTLIB_AVAILABLE:
        try:
            print("\nGenerating visualizations...")
            plot_season_statistics(season_stats)
            plot_character_dialogue(character_stats)
            print("Analysis complete! Check the generated PNG files for visualizations.")
        except Exception as e:
            print(f"Error creating visualizations: {e}")
    else:
        print("\nSkipping visualizations (matplotlib not available)")
        print("To enable visualizations, install matplotlib with: pip install matplotlib")

if __name__ == "__main__":
    main()
