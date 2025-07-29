import unittest
from worldmapper import WorldMapper

class TestWorldMapper(unittest.TestCase):
    
    def setUp(self):
        self.wm = WorldMapper()
    
    def test_get_all_countries(self):
        countries = self.wm.get_all_countries()
        self.assertIsInstance(countries, list)
        self.assertGreater(len(countries), 0)
    
    def test_get_country_by_name(self):
        country = self.wm.get_country_by_name("American Samoa")
        self.assertIsNotNone(country)
        self.assertEqual(country['alpha2'], 'AS')
    
    def test_get_country_by_alpha2(self):
        country = self.wm.get_country_by_alpha2("AS")
        self.assertIsNotNone(country)
        self.assertEqual(country['name'], 'American Samoa')
    
    def test_search_countries(self):
        results = self.wm.search_countries("samoa")
        self.assertGreater(len(results), 0)

if __name__ == '__main__':
    unittest.main()