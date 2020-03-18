import io

from shishakai import MovieWalker


def dummy_html_stream(dummy_url):
    html = """
    <div class="previewMovieInfo">
      <h3><a href="/shisyakai/12345/">XXX試写会(100組200名様)</a></h3>
      <table>
        <tr>
          <th>応募締切</th>
          <td>1970年1月1日(木)</td>
        </tr>
        <tr>
          <th>開催日時</th>
          <td>1月8日(木) 開場 18:30/開映 19:00</td>
        </tr>
        <tr>
          <th>開催場所</th>
          <td>東京某所 (東京都港区xxx)</td>
        </tr>
      </table>
    </div>
    """
    return io.StringIO(html)


class TestMovieWalker:
    def test_events(self, monkeypatch):
        movie_walker = MovieWalker()
        with monkeypatch.context() as m:
            m.setattr("shishakai.base.urlopen", dummy_html_stream)
            events = movie_walker.events

        assert len(events) == 1
        assert events[0]["title"] == "XXX試写会(100組200名様)"
        assert events[0]["url"] == "https://movie.walkerplus.com/shisyakai/12345/"
        assert events[0]["deadline"] == "1970年1月1日(木)"
        assert events[0]["date_and_time"] == "1月8日(木) 開場 18:30/開映 19:00"
        assert events[0]["venue"] == "東京某所 (東京都港区xxx)"
