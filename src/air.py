from abc import ABC, abstractmethod

class Aircrafts(ABC):
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

    @abstractmethod
    def work_air(self):
        pass


class Aircraft(Aircrafts):
    aircraft_list: []


    lat: float
    lon: float
    alt: int
    vel: float
    gov: str


    def __init__(self, lat, lon, alt, vel, gov):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.vel = vel
        self.gov = gov


    def work_air(self):
        print(f'{self.gov}: H={self.alt} м, V={self.vel}')


    def __str__(self):
        return f'Гос:{self.gov} Гео:{self.lon}/{self.lat} V={self.vel} H={self.alt}  '


    @classmethod
    def search_aircraft(cls, air_list, num=None):
        if num is not None:
            air_list = air_list[:num]

        cls.aircraft_list = [
            cls(item['lat'], item['lon'], item['alt'], item['vel'], item['gov'])
            for item in air_list
        ]
        return cls.aircraft_list
