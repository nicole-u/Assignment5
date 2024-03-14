from urllib import error
import unittest
from Last_FM import LastFM as fm

USERNAME = "nutamaaaaa"
FM_API_KEY = "c0a60fb3ace4ff1ea2748e5319a9ee72"

class RegularTest(unittest.TestCase):
    """
    Calling everything regularly.
    I have not touched LastFM since
    setting these parameters, they 
    should stay the same.
    """
    def test_regular(self):
        last_fm = fm(USERNAME)
        last_fm.set_apikey(FM_API_KEY)
        last_fm.load_data()
        assert last_fm.fav_artist == "Vivid BAD SQUAD"
        assert last_fm.fav_track == "フラジール (feat. 東雲彰人&青柳冬弥)"

class DownloadURL(unittest.TestCase):
    """
    Downloading URL and causing errors
    on purpose.
    """
    def test_url(self):
        url_test = fm(USERNAME)
        url_test.set_apikey(FM_API_KEY)
        try:
            url_test._download_url("https://www.thisisnotlastfm.com")
        except error.HTTPError:
            print("URL Error caught.")

class NoUsernameParam(unittest.TestCase):
    """
    Testing with no username.
    """
    def test_no_user(self):
        no_user = fm()
        try:
            no_user.set_apikey(FM_API_KEY)
            no_user.load_data()
            print("No username error successfully caught.")
        except ValueError or TypeError:
            print("Something went wrong with error handling in API")

class WrongAPIKey(unittest.TestCase):
    """
    Testing with the wrong API key
    """
    def test_wrongAPIKey(self):
        wrong_api_key = fm(USERNAME)
        wrong_api_key.set_apikey("not_an_api_key_lol")
        wrong_api_key.load_data()
        assert wrong_api_key.fav_track is None
        assert wrong_api_key.fav_artist is None

class NoAPIKey(unittest.TestCase):
    """
    Testing with no API key
    """
    def test_no_key(self):
        no_api_key = fm(USERNAME)
        try:
            no_api_key.load_data()
            print("No API Key errors successfully caught in API")
        except ValueError or TypeError:
            print("Something went wrong with error handling.")

class TranscludeTest(unittest.TestCase):
    """
    Testing transclude function
    """
    def test_transclude(self):
        transclude_time = fm(USERNAME)
        transclude_time.set_apikey(FM_API_KEY)
        transclude_time.load_data()
        print(transclude_time.transclude("test @lastfm"))
        try:
            print(transclude_time.transclude("Test @llastfmm"))
            print(transclude_time.transclude("No keyword lol"))
        except ValueError:
            print("Transclusion errors successfully caught.")

if __name__ == "__main__":
    unittest.main()
