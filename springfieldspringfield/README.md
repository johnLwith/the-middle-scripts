# The Middle Scripts Scraper

A Python script to scrape episode scripts from the TV show "The Middle" from [www.springfieldspringfield.co.uk](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-middle)

## Status

Pending

## Features

- Scrapes all available episode scripts from "The Middle"
- Organizes scripts by season and episode
- Saves scripts with metadata (title and source URL)

## Requirements

- Python 3.x
- Required Python packages:
  ```
  requests
  beautifulsoup4
  ```

To install required packages:
```bash
uv venv && source .venv/bin/activate &&
uv pip install requests beautifulsoup4
```

## Usage

### Scraping Scripts

1. Clone this repository or download the script files
2. Install the required packages
3. Run the scraping script:
```bash
python3 scrape_the_middle.py
```

The script will:
- Create a directory called `the_middle_scripts`
- Create subdirectories for each season
- Download and save scripts for all available episodes
- Show progress information during the download

### Analyzing Scripts

After scraping the scripts, you can analyze them using the analysis tool:
```bash
python3 analyze_scripts.py
```

The analysis script provides:
- Word count statistics for each season
- Average words per episode
- Character dialogue analysis
- Visual representation of the data (requires matplotlib)

Additional requirements for analysis:
```bash
pip install matplotlib
```

## Output Structure

```
the_middle_scripts/
├── Season_1/
│   ├── 01_Episode_Title.txt
│   ├── 02_Episode_Title.txt
│   └── ...
├── Season_2/
│   ├── 01_Episode_Title.txt
│   ├── 02_Episode_Title.txt
│   └── ...
└── ...
```

Each script file contains:
- Episode title
- Source URL
- Complete episode script

## Notes

- The script includes a 1-second delay between requests to avoid overwhelming the server
- Some episodes might be missing due to unavailability on the source website
- The script uses a user agent header to mimic a web browser

## Limitations

- Depends on the website's structure remaining consistent
- Some episodes might be missing from the source website
- Network issues might interrupt the scraping process
- Rate limiting might increase the total scraping time

## Legal Notice

This script is for educational purposes only. Make sure to comply with the website's terms of service and robots.txt file when using web scraping tools.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.


---
Powered by vscode plugins:
- [Augment]