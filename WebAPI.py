from abc import ABC, abstractmethod
from urllib import request, error
import json
import requests

class WebAPI(ABC):
    """
    Abstract parent class that handles all communication
    with online web APIs.
    """
    def _download_url(self, url_to_download: str) -> dict:
        """
        Method to download the info from the url
        """
        response = None
        r_obj = None

        try:
            response = request.urlopen(url_to_download)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except error.HTTPError as e:
            print('Failed to download contents of URL.')
            print(f'Status code: {e.code}')

        except requests.ConnectionError:
            print("Could not connect to server.")

        except error.URLError as err:
            print("Error with URL.")
            print(f"Status code: {err}")

        except json.JSONDecodeError:
            print("Error with JSON file.")

        except requests.exceptions.RequestException as e:
            print("An error occurred.")
            print("Error:", e)

        finally:
            if response is not None:
                response.close()

        return r_obj

    def set_apikey(self, apikey:str) -> None:
        """
        Method to set the API key
        """
        self.api_key = apikey

        return self.api_key

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def transclude(self, message:str) -> str:
        pass
