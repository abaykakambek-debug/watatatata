"""Deal Radar: scrape the first 20 books from the educational website."""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_html(url: str = BASE_URL) -> str:
    """Download HTML and raise an exception for network/HTTP errors."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding
    return response.text


def parse_books(html: str, base_url: str = BASE_URL, limit: int = 20) -> list[dict]:
    """Parse book cards into dictionaries without performing network requests."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("article.product_pod")
    books = []

    for card in cards[:limit]:
        title_element = card.select_one("h3 a")
        price_element = card.select_one(".price_color")
        rating_element = card.select_one("p.star-rating")
        if not all((title_element, price_element, rating_element)):
            continue

        title = title_element.get("title") or title_element.get_text(strip=True)
        price = price_element.get_text(strip=True)
        rating_classes = rating_element.get("class", [])
        rating = next((RATINGS[name] for name in rating_classes if name in RATINGS), None)
        if rating is None:
            continue

        books.append({
            "title": title.strip(),
            "price": price,
            "rating": rating,
            "url": urljoin(base_url, title_element.get("href", "")),
        })
    return books


def print_books(books: list[dict]) -> None:
    print(f"\nDEAL RADAR — найдено {len(books)} книг\n")
    print(f"{'№':<4} {'Название':<43} {'Цена':<12} {'Рейтинг':<8}")
    print("-" * 72)
    for index, book in enumerate(books, 1):
        title = book["title"][:41]
        print(f"{index:<4} {title:<43} {book['price']:<12} {book['rating']}/5")


def main() -> None:
    try:
        html = fetch_html()
        books = parse_books(html)
    except requests.RequestException as exc:
        print(f"Ошибка HTTP-запроса: {exc}")
        raise SystemExit(1) from exc

    if not books:
        print("Книги не найдены. Проверьте HTML и CSS-селекторы.")
        raise SystemExit(1)
    print_books(books)
    if len(books) != 20:
        print("Внимание: найдено меньше 20 книг. Проверьте структуру страницы.")


if __name__ == "__main__":
    main()
