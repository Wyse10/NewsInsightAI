import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_tv3_news():
    base_url = "https://3news.com"
    url = f"{base_url}/category/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = [urljoin(base_url, a["href"]) for a in soup.find_all("a", href=True) if "/news/" in a["href"]]
    links = list(set(links))

    articles = []
    for link in links:
        try:
            art_res = requests.get(link, timeout=10)
            art_soup = BeautifulSoup(art_res.text, "html.parser")

            title = art_soup.find("h1").get_text(strip=True) if art_soup.find("h1") else "No title"

            paragraphs = []
            for p in art_soup.find_all("p"):
                if not p.find("a") and p.get_text(strip=True):
                    paragraphs.append(p.get_text(strip=True))

            body = " ".join(paragraphs)
            if body:
                articles.append((title, body))
        except Exception as e:
            print(f"Error scraping {link}: {e}")

    return articles

