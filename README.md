# Book_Scraper

A web scraper that crawls the site https://books.toscrape.com and stores book title → price entries as newline-delimited JSON (JSON Lines).

## What it does
- Crawls the site starting at https://books.toscrape.com
- Extracts each book's title and price from listing pages
- Follows pagination automatically until no "next" page is found
- Writes the results into book_prices.jsonl (one JSON object per line)

## Where data is stored
- Output file: `book_prices.jsonl` in the repository root
- Format: JSON Lines (each line is one JSON object). Example line:

  {"A Light in the Attic": "£51.77"}

- Note: running the script overwrites `book_prices.jsonl` (the script opens the file with mode "w").

## Prerequisites
- Python 3.8+
- pip (or pip3)

## Installing dependencies
The repository includes a `requirements.txt` file. If it is empty, the project requires at least:

- requests
- beautifulsoup4

Recommended (matches the virtualenv that may be included):

requests==2.34.2
beautifulsoup4==4.15.0

To install from `requirements.txt`:

1. (Optional) Create and activate a virtual environment:

   python3 -m venv scraping_venv
   source scraping_venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

If `requirements.txt` is empty, install packages directly and then freeze to the file:

   pip install requests beautifulsoup4
   pip freeze > requirements.txt

## Usage
Run the scraper from the repository root:

   python3 scraper.py

Expected output: a file named `book_prices.jsonl` is created/overwritten containing a JSON object per line mapping a book title to its price.

## Customization
- Change start URL: edit the call to `book_crawler()` near the bottom of `scraper.py`.
- Change output filename: edit the filename passed to `file_writer()` in `scraper.py`.
- Adjust crawl delay / retries by modifying `time.sleep()` calls and `fetch_page()` arguments.

## Notes and caveats
- This scraper targets the educational demo site `books.toscrape.com`. When scraping other sites, check and respect their robots.txt and terms of service.
- The script uses a single-worker, polite delay between requests (1 second) and a small retry/backoff strategy.

## Troubleshooting
- If requests fail, check your network and whether the site is reachable.
- If you see encoding issues, ensure UTF-8 is used (script opens output with `encoding='utf-8'`).

## Acknowledgements
Built with requests and BeautifulSoup.

