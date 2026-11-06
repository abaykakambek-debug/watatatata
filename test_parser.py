import unittest

from main import parse_books

SAMPLE_HTML = '''
<html><body>
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="catalogue/sample_1/index.html" title="Python &amp; Web">Short</a></h3>
  <p class="price_color">£19.99</p>
</article>
<article class="product_pod">
  <p class="star-rating Five"></p>
  <h3><a href="catalogue/second_2/index.html" title="Second Book">Second</a></h3>
  <p class="price_color">£12.50</p>
</article>
</body></html>
'''


class ParseBooksTests(unittest.TestCase):
    def test_extracts_title_price_rating_and_url(self):
        books = parse_books(SAMPLE_HTML)
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]["title"], "Python & Web")
        self.assertEqual(books[0]["price"], "£19.99")
        self.assertEqual(books[0]["rating"], 3)
        self.assertEqual(books[0]["url"], "https://books.toscrape.com/catalogue/sample_1/index.html")
        self.assertEqual(books[1]["rating"], 5)

    def test_limit(self):
        self.assertEqual(len(parse_books(SAMPLE_HTML, limit=1)), 1)

    def test_empty_html(self):
        self.assertEqual(parse_books("<html></html>"), [])


if __name__ == "__main__":
    unittest.main()
