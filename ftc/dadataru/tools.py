from dadata import Dadata


class DaData(Dadata):

    def get_address_by_geolocate(self, latitude, longitude, radius_meters=50):
        result = self.geolocate(name='address',
                                lat=float(latitude),
                                lon=float(longitude),
                                radius_meters=radius_meters)
        return result

    def get_address(self, q):
        result = self.suggest('address', q, count=20)
        return result
