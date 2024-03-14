from WebAPI import WebAPI
from OpenWeather import OpenWeather
from Last_FM import LastFM

API_KEY_WEATHER = "37678f5231ba3e6702a5bf80a140f947"
API_KEY_FM = "c0a60fb3ace4ff1ea2748e5319a9ee72"

def test_api(message: str, apikey: str, webapi: WebAPI):
    """
    Function to test the API.
    """
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)

opw = OpenWeather()
lastfm = LastFM()

test_api("Testing @weather", API_KEY_WEATHER, opw)
test_api("Testing @lastfm", API_KEY_FM, lastfm)
