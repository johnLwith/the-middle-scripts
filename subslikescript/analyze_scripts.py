import os
import re
import matplotlib.pyplot as plt

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
        dict: A dictionary with season numbers as keys and word count statistics as values.
    """
    season_stats = {}
    for season_dir in os.listdir(scripts_dir):
        if season_dir.startswith('Season_'):
            season_num = int(season_dir.split('_')[1])
            episode_word_counts = []
            season_dir_path = os.path.join(scripts_dir, season_dir)
            for episode_file in os.listdir(season_dir_path):
                if episode_file.endswith('.txt'):
                    file_path = os.path.join(season_dir_path, episode_file)
                    word_count = count_words_in_file(file_path)
                    episode_word_counts.append(word_count)
            if episode_word_counts:
                total_words = sum(episode_word_counts)
                avg_words_per_episode = total_words / len(episode_word_counts)
                season_stats[season_num] = {
                    'total_words': total_words,
                    'avg_words_per_episode': avg_words_per_episode,
                    'episode_counts': len(episode_word_counts)
                }
    return season_stats

def plot_season_stats(season_stats):
    """
    Plot the total words per season and average words per episode.

    Args:
        season_stats (dict): A dictionary with season numbers as keys and word count statistics as values.
    """
    seasons = sorted(season_stats.keys())
    total_words = [season_stats[season]['total_words'] for season in seasons]
    avg_words = [season_stats[season]['avg_words_per_episode'] for season in seasons]

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(seasons, total_words)
    plt.title('Total Words per Season')
    plt.xlabel('Season')
    plt.ylabel('Total Words')

    plt.subplot(1, 2, 2)
    plt.bar(seasons, avg_words)
    plt.title('Average Words per Episode')
    plt.xlabel('Season')
    plt.ylabel('Average Words')

    plt.tight_layout()
    plt.show()

def analyze_characters(scripts_dir):
    """
    Analyze character dialogue in all scripts.

    Args:
        scripts_dir (str): The directory containing season subdirectories.

    Returns:
        dict: A dictionary with character names as keys and word counts as values.
    """
    character_word_counts = {}
    for season_dir in os.listdir(scripts_dir):
        if season_dir.startswith('Season_'):
            season_dir_path = os.path.join(scripts_dir, season_dir)
            for episode_file in os.listdir(season_dir_path):
                if episode_file.endswith('.txt'):
                    file_path = os.path.join(season_dir_path, episode_file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            # Skip metadata (title and source URL)
                            lines = content.split('\n')[2:]
                            current_character = None
                            for line in lines:
                                if ':' in line:
                                    parts = line.split(':', 1)
                                    if len(parts) == 2:
                                        character = parts[0].strip().upper()
                                        dialogue = parts[1].strip()
                                        if character:
                                            current_character = character
                                            words = re.findall(r'\w+', dialogue.lower())
                                            character_word_counts[current_character] = character_word_counts.get(current_character, 0) + len(words)
                                elif current_character:
                                    words = re.findall(r'\w+', line.lower())
                                    character_word_counts[current_character] = character_word_counts.get(current_character, 0) + len(words)
                    except FileNotFoundError:
                        print(f"File {file_path} not found.")
    return character_word_counts

def plot_character_stats(character_word_counts, top_n=10):
    """
    Plot the top N characters with the most dialogue.

    Args:
        character_word_counts (dict): A dictionary with character names as keys and word counts as values.
        top_n (int): The number of top characters to display.
    """
    sorted_characters = sorted(character_word_counts.items(), key=lambda item: item[1], reverse=True)[:top_n]
    characters = [char[0] for char in sorted_characters]
    word_counts = [char[1] for char in sorted_characters]

    plt.figure(figsize=(10, 6))
    plt.bar(characters, word_counts)
    plt.title(f'Top {top_n} Characters by Word Count')
    plt.xlabel('Character')
    plt.ylabel('Word Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    scripts_dir = 'the_middle_scripts'
    if not os.path.exists(scripts_dir):
        print(f"Directory {scripts_dir} not found. Please run the scraping script first.")
        return

    # Analyze seasons
    season_stats = analyze_seasons(scripts_dir)
    print("Season Statistics:")
    for season in sorted(season_stats.keys()):
        stats = season_stats[season]
        print(f"Season {season}:")
        print(f"  Total Words: {stats['total_words']}")
        print(f"  Average Words per Episode: {stats['avg_words_per_episode']:.2f}")
        print(f"  Episode Count: {stats['episode_counts']}")

    # Plot season statistics
    plot_season_stats(season_stats)

    # Analyze characters
    character_word_counts = analyze_characters(scripts_dir)
    print("\nTop Character Dialogue Analysis:")
    sorted_characters = sorted(character_word_counts.items(), key=lambda item: item[1], reverse=True)[:10]
    for character, word_count in sorted_characters:
        print(f"  {character}: {word_count} words")

    # Plot character statistics
    plot_character_stats(character_word_counts)

if __name__ == "__main__":
    main()
