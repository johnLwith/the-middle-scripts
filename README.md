# The Middle Scripts

A collection of Python scrapers to extract episode scripts from the TV show "The Middle" from multiple sources.

## Differences
[diff.md](diff.md)

## 🎯 Available Scrapers

### 1. Springfield Springfield Scraper ✅ **COMPLETE**
**Location**: `springfieldspringfield/`
**Source**: [www.springfieldspringfield.co.uk](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-middle)

- ✅ **214 episodes** across 9 seasons
- ✅ Complete implementation with analysis tools
- ✅ Test mode for validation
- ✅ Advanced visualizations
- ✅ 100% success rate

### 2. Subslikescript Scraper ✅ **COMPLETE**
**Location**: `subslikescript/`
**Source**: [subslikescript.com](https://subslikescript.com/series/The_Middle-1442464)

- ✅ Most episodes available (missing Season 6)
- ✅ Working implementation
- ✅ Basic analysis tools
- ✅ Established and tested

### 3. My-Subs Subtitle Scraper ✅ **COMPLETE**
**Location**: `my-subs/`
**Source**: [my-subs.co](https://my-subs.co/showlistsubtitles-1702-the-middle)

- ✅ **214 episodes** across 9 seasons
- ✅ English subtitles only
- ✅ SRT to TXT conversion
- ✅ Organized by season folders
- ✅ **SXXEXX.txt** naming format

## 🚀 Quick Start

### Springfield Springfield (Recommended)
```bash
source venv/bin/activate
cd springfieldspringfield/
pip install requests beautifulsoup4 matplotlib
python3 scrape_springfield.py --test  # Test first
python3 scrape_springfield.py         # Full scrape
python3 analyze_scripts.py            # Analyze results
```

### Subslikescript (Alternative)
```bash
source venv/bin/activate
cd subslikescript/
pip install requests beautifulsoup4 matplotlib
python3 scrape_the_middle.py
python3 analyze_scripts.py
```

### My-Subs (English Subtitles)
```bash
cd my-subs/
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4
python3 scrape.py                     # Download SRT files
python3 organize.py                   # Convert to TXT format
```
Output: `my-subs/my_subtitles/Season_X/SXXEXX.txt`

## 📊 Comparison

| Feature | Springfield Springfield | Subslikescript | My-Subs |
|---------|------------------------|----------------|---------|
| **Status** | ✅ Complete | ✅ Complete | ✅ Complete |
| **Episodes** | 214 (all 9 seasons) | ~190 (missing Season 6) | 214 (all 9 seasons) |
| **Content** | Scripts/Transcripts | Scripts/Transcripts | English Subtitles |
| **Test Mode** | ✅ Available | ❌ Not available | ❌ Not available |
| **Analysis** | ✅ Advanced | ✅ Basic | ❌ None |
| **Visualizations** | ✅ Comprehensive | ✅ Standard | ❌ None |
| **Success Rate** | 100% | ~95% | 100% |

## 📁 Output Structure

Scrapers create organized directory structures:

### Springfield Springfield & Subslikescript
```
{scraper}_scripts/
├── Season_1/
│   ├── 01_Episode_Title.txt
│   ├── 02_Episode_Title.txt
│   └── ...
└── Season_9/
    └── ...
```

Each script file contains:
- Episode title and metadata
- Source URL
- Complete episode transcript
- Character dialogue and stage directions

### My-Subs
```
my-subs/my_subtitles/
├── Season_1/
│   ├── S01E01.txt
│   ├── S01E02.txt
│   └── ...
└── Season_9/
    └── ...
```

Each subtitle file contains:
- Title and source metadata
- Cleaned dialogue text (timestamps removed)
- English subtitles only

## 🔧 Requirements

- Python 3.x
- Required packages:
  ```bash
  pip install requests beautifulsoup4 matplotlib
  ```

## 📈 Analysis Features

Both implementations include analysis tools:

- **Word count statistics** per episode and season
- **Character dialogue frequency** analysis
- **Visual charts and graphs** (requires matplotlib)
- **Season comparison** tools
- **Export capabilities** for further analysis

## 🛠️ Development

### Project Structure
```
the-middle-scripts/
├── springfieldspringfield/     # Springfield Springfield scraper
│   ├── scrape_springfield.py   # Main scraper
│   ├── analyze_scripts.py      # Analysis tools
│   └── README.md              # Detailed documentation
├── subslikescript/            # Subslikescript scraper
│   ├── scrape_the_middle.py   # Main scraper
│   ├── analyze_scripts.py     # Analysis tools
│   └── README.md             # Documentation
└── README.md                 # This file
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests! Contributions welcome for:
- Resume functionality for interrupted scraping
- Additional analysis features
- Performance optimizations
- Bug fixes and improvements
- New data sources

## ⚖️ Legal Notice

This project is for educational purposes only. Make sure to comply with the websites' terms of service and robots.txt files when using web scraping tools.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
*Powered by 
- [Augment] - sprintfieldspringfield
- [CodeBuddy] - subslikescript
- [Trae] - subslikescript


