import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"
r = requests.get(url, timeout=10)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

for card in soup.select("article.product_pod")[:20]:
    title = card.select_one("h3 a")["title"]
    price = card.select_one(".price_color").get_text(strip=True)
    rating = card.select_one(".star-rating")["class"][1]
    print(f"{title:45} {price:8} {rating}")
