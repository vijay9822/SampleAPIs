import unittest
import requests


class TestCases(unittest.TestCase):
    url_list = ['/players-on-or-after/1998', '/avg-age-of-players-in-different-teams', '/max-left-handed-in-country',
                '/country-null', '/players-in-country/Australia']

    def test_apis(self):
        api_localhost_add = 'http://127.0.0.1:5000'
        for url in TestCases.url_list:
            r = requests.get(api_localhost_add + url)
            self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
