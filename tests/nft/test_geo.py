
# Copyright (c) 2022 Tolam Earth
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

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
