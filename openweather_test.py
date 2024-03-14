import unittest
from urllib import error
from OpenWeather import OpenWeather
from WebAPI import WebAPI

ZIPCODE = "90703"
CCODE = "US"
WEATHER_APIKEY = "37678f5231ba3e6702a5bf80a140f947"


class RegularTest(unittest.TestCase):
    """
    Calling everything properly.
    """
    def test_regular(self):
        open_weather = OpenWeather(ZIPCODE, CCODE)
        open_weather.set_apikey(WEATHER_APIKEY)
        open_weather.load_data()
        assert open_weather.city == "Cerritos"
        assert open_weather.longitude == -118.0686
        assert open_weather.latitude == 33.8669


class DownloadURL(unittest.TestCase):
    """
    Downloading URL test
    """
    def test_url(self):
        url_test = OpenWeather(ZIPCODE, CCODE)
        url_test.set_apikey(WEATHER_APIKEY)
        try:
            url_test._download_url("https://www.thisisnotopenweather.com")
        except error.HTTPError:
            print("URL Error caught.")

class WrongAPIKey(unittest.TestCase):
    """
    Calling the wrong API key
    """
    def test_wrongAPIKey(self):
        wrong_api_key = OpenWeather(ZIPCODE, CCODE)
        wrong_api_key.set_apikey("not_an_api_key_lol")
        wrong_api_key.load_data()
        assert wrong_api_key.longitude is None
        assert wrong_api_key.latitude is None
        assert wrong_api_key.temperature is None
        assert wrong_api_key.description is None
        assert wrong_api_key.city is None
        assert wrong_api_key.sunset is None


class NoParameters(unittest.TestCase):
    """
    Calling with no parameters
    """
    def test_no_params(self):
        no_param_weather = OpenWeather()
        no_param_weather.set_apikey(WEATHER_APIKEY)
        no_param_weather.load_data()
        assert no_param_weather.city == "Irvine"
        assert no_param_weather.longitude == -117.8417
        assert no_param_weather.latitude == 33.6425


class TranscludeTest(unittest.TestCase):
    """
    Testing transclude function
    """
    def test_transclude(self):
        transclude_time = OpenWeather(ZIPCODE, CCODE)
        transclude_time.set_apikey(WEATHER_APIKEY)
        transclude_time.load_data()
        print(transclude_time.transclude("test @weather"))
        try:
            print(transclude_time.transclude("Test @weether"))
            print(transclude_time.transclude("No keyword lol"))
        except ValueError:
            print("Transclusion errors successfully caught.")


class NoAPIKey(unittest.TestCase):
    """
    Testing without an API key
    """
    def test_no_key(self):
        no_api_key = OpenWeather(ZIPCODE, CCODE)
        try:
            no_api_key.load_data()
        except ValueError:
            print("No API Key Error successfully caught.")


if __name__ == "__main__":
    unittest.main()
