from django.test import TestCase
from utils import geo_controller


class GeoControllerTest(TestCase):

    def setUp(self):
        self.query1 = '116 memon place'
        self.query2 = 'iwegowengowneog'

    def test_happy(self):
        """Test is location dictionary is returned"""
        actual = geo_controller.geocode(self.query1)
        expected = {'lat': 43.9048502, 'lng': -79.2828746}
        self.assertDictEqual(actual, expected)

    def test_exception(self):
        """Test if exception is raised upon invalid query"""
        self.assertRaises(ValueError, geo_controller.geocode, self.query2)
