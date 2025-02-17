import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(url, a_tag['href'])
        links.add(link)
    return links

def scrape_website(base_url):
    visited = set()
    to_visit = {base_url}
    all_texts = []

    while to_visit:
        url = to_visit.pop()
        if url not in visited:
            visited.add(url)
            print(f"Scraping {url}")
            try:
                text = scrape_page(url)
                all_texts.append(text)
                links = get_all_links(url)
                to_visit.update(links - visited)
            except Exception as e:
                print(f"Error scraping {url}: {e}")

    return all_texts

base_url = "https://en.wikipedia.org/wiki/Web_scraping"
all_texts = scrape_website(base_url)

