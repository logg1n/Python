import unittest
from unittest.mock import patch
import requests

def get_random_cat_image() -> str | None:
    url = "https://api.thecatapi.com/v1/images/search"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and "url" in data[0]:
                return data[0]["url"]
        return None
    except requests.RequestException:
        return None



class TestGetRandomCatImage(unittest.TestCase):

    @patch("requests.get")
    def test_successful_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"url": "https://cdn2.thecatapi.com/images/abc.jpg"}]

        result = get_random_cat_image()
        self.assertEqual(result, "https://cdn2.thecatapi.com/images/abc.jpg")

    @patch("requests.get")
    def test_failed_response_404(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {}

        result = get_random_cat_image()
        self.assertIsNone(result)

    @patch("requests.get")
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException

        result = get_random_cat_image()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
