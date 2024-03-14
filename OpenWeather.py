"""
A class that helps handle connection and data
downloading from the OpenWeather online API.
"""

import WebAPI
DEV_API_KEY = "37678f5231ba3e6702a5bf80a140f947"

def kelvin_to_fahrenheit(k_temp):
    """
    A function that takes Kelvin temperatures and converts
    them to Fahrenheit.
    """
    f_temp = round((float(k_temp) - 273.15) * 9/5 + 32)
    return f_temp


class OpenWeather(WebAPI.WebAPI):
    """
    A class that handles getting the data
    from the OpenWeather API and passes it
    to class data attributes to be used later.
    """
    def __init__(self, zipcode="92617", ccode="US"):
        self.api_key = None
        self.zipcode = zipcode
        self.country = ccode
        self.temperature = None
        self.high_temp = None
        self.low_temp = None
        self.longitude = None
        self.latitude = None
        self.description = None
        self.humidity = None
        self.city = None
        self.sunset = None

    def _download_url(self, url_to_download: str) -> dict:
        downloaded = WebAPI.WebAPI._download_url(self, url_to_download)
        return downloaded

    def set_apikey(self, apikey: str):
        try:
            WebAPI.WebAPI.set_apikey(self, apikey)
        except:
            print("Error with API key.")
            WebAPI.WebAPI.set_apikey(self, DEV_API_KEY)

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response
        in class data attributes.
        '''
        if self.api_key is None:
            raise ValueError("No API key has been inputted.")
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.country}&appid={self.api_key}"
        returned_data = self._download_url(url)
        try:
            self.longitude = returned_data['coord']['lon']
            self.latitude = returned_data['coord']['lat']
            self.description = returned_data['weather'][0]['description']
            self.temperature = kelvin_to_fahrenheit(returned_data['main']['temp'])
            self.high_temp = kelvin_to_fahrenheit(returned_data['main']['temp_max'])
            self.low_temp = kelvin_to_fahrenheit(returned_data['main']['temp_min'])
            self.humidity = returned_data['main']['humidity']
            self.city = returned_data['name']
            self.sunset = returned_data['sys']['sunset']
        except TypeError:
            print("Data retrieval failure because of an error with the URL.")

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        keyword = "@weather"
        if keyword not in message:
            raise ValueError("No keyword found in message.")
        transcluded_msg = message.replace(keyword, self.description)
        return transcluded_msg
