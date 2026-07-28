import requests as r
from bs4 import BeautifulSoup as bs
import json
import time
from urllib.parse import urljoin

def fetch_page(url,retries=3,backoff_factor=2):

    for attempt in range(retries):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            resp = r.get(url,timeout = 15,headers=headers)
            resp.raise_for_status()
            return resp
        except (r.exceptions.RequestException, r.exceptions.Timeout) as e:
            if attempt == retries - 1:
                print(f"Failed to fetch {url} after {retries} attempts: {e}")
                return None
            time.sleep(backoff_factor**attempt)

def book_crawler(url: str):
    nxt_url = url

    while nxt_url:
        resp = fetch_page(nxt_url)
        if not resp:
            print(f"Stopping crawl early due to network failure at {nxt_url}")
            break
        time.sleep(1)

        html = resp.content
        
        soup = bs(html,"html.parser")
        for book in soup.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3"):
            title_element = book.select_one("h3 > a ")
            if title_element:
                title = title_element.get_text().strip()
            else:
                title = "Title not found"
            price_element = book.select_one("div.product_price > p.price_color")
            if price_element:
                price = price_element.get_text().strip()
            else:
                price = "Price not found"
            yield {title: price}

        nxt_btn = soup.select_one("ul.pager > li.next > a")
        if nxt_btn:
            link = nxt_btn.get("href")
            nxt_url = urljoin(nxt_url,link)
        else:
            nxt_url = None




def file_writer(filename, data_stream):
    try:
        with open(filename, "w", encoding="utf-8") as fp:
            for data in data_stream:
                json_data = json.dumps(data, ensure_ascii=False)
                fp.write(json_data+"\n")
            else:
                return True

    except Exception as e:
        print(f"Error {e}")
        return False


if __name__ == "__main__":
    gen_obj = book_crawler("https://books.toscrape.com")

    if file_writer("book_prices.jsonl", gen_obj):
        print("successfully stored the data.")
    else:
        print("An error occured")