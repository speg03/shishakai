from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup


class MovieWalker:
    def __init__(self):
        self.base_url = "https://movie.walkerplus.com/shisyakai/"

    def events(self):
        html = urlopen(self.base_url).read()
        bs = BeautifulSoup(html, "html.parser")
        return [
            self._parse_item(item)
            for item in bs.find_all("div", class_="previewMovieInfo")
        ]

    def _parse_item(self, item):
        title = item.a.string
        url = urljoin(self.base_url, item.a["href"])
        table_values = item.table.find_all("td")
        return {
            "title": title,
            "url": url,
            "deadline": table_values[0].string,
            "date_and_time": table_values[1].string,
            "venue": table_values[2].string,
        }
