import pytest

from hem.armm import geo


class TestGeoCoder:
    geocoder = geo.GeoCoder()

    def test_missouri(self):
        lon, lat = self.geocoder.geocode('USA', 'MO')
        assert lon == pytest.approx(-92.498918, rel=1e-6)
        assert lat == pytest.approx(38.319047, rel=1e-6)

    def test_paris(self):
        lon, lat = self.geocoder.geocode('FRA', '75C')
        assert lon == pytest.approx(2.350184, rel=1e-6)
        assert lat == pytest.approx(48.856001, rel=1e-6)

    def test_not_found(self):
        lon, lat = self.geocoder.geocode('XYZ', 'QRS')
        assert lon is None
        assert lat is None

    def test_caching(self):
        # fresh geocoder
        geocoder = geo.GeoCoder()
        geocoder.geocode(country='USA', first_subdivision='MO')
        cache_info = geocoder.geocode.cache_info()
        assert cache_info.hits == 0

        geocoder.geocode(country='USA', first_subdivision='MO')
        assert geocoder.geocode.cache_info().hits == 1
