from django.db import models
from math import cos, sqrt, radians
import requests
from urllib.parse import quote
import xml.etree.ElementTree as ET
from django.contrib.auth.models import User 

HKU_LOCATIONS = {
    'Main Campus': (22.28405, 114.13784),
    'Sassoon Road Campus': (22.26725, 114.12881),
    'Swire Institute of Marine Science': (22.20805, 114.26021),
    'Kadoorie Centre': (22.43022, 114.11429),
    'Faculty of Dentistry': (22.28649, 114.14426)
}
EARTH_RADIUS = 6371  # 公里
ALS_ENDPOINT = 'https://www.als.gov.hk/lookup'

class Accommodation(models.Model):
    address = models.CharField(max_length=255, primary_key=True)
    address = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=50)
    period_of_availability = models.CharField(max_length=100)
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.FloatField(null=True, blank=True)  # computed field (optional)

    # Geo information (from HK ALS API)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geo_address = models.CharField(max_length=255, null=True, blank=True)


    def fetch_location_data(self):
        # params = {'q': self.address, 'n': 1}
        # headers = {'Accept': 'application/json'}
        # try:
        #     response = requests.get(ALS_ENDPOINT, params=params, headers=headers)
        #     if response.status_code == 200:
        #         data = response.json()
        #         if data and isinstance(data, list) and len(data) > 0:
        #             result = data[0]
        #             geo_info = result.get('GeospatialInformation', {})
        #             self.latitude = float(geo_info.get('Latitude'))
        #             self.longitude = float(geo_info.get('Longitude'))
        #             self.geo_address = result.get('GeoAddress')
        # except Exception as e:
        #     print(f"Address lookup failed: {e}")
        params = {'q': self.address, 'n': 1}
        try:
            response = requests.get(ALS_ENDPOINT, params=params)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                geo_address = root.find('.//GeoAddress')
                lat = root.find('.//Latitude')
                lon = root.find('.//Longitude')
                if geo_address is not None:
                    self.geo_address = geo_address.text
                if lat is not None:
                    self.latitude = float(lat.text)
                if lon is not None:
                    self.longitude = float(lon.text)
        except Exception as e:
            print(f"[ALS Lookup Error] {e}")        

    def calculate_distance(self, ref_lat, ref_lon):
        if self.latitude is not None and self.longitude is not None:
            lat1 = radians(ref_lat)
            lon1 = radians(ref_lon)
            lat2 = radians(self.latitude)
            lon2 = radians(self.longitude)
            x = (lon2 - lon1) * cos((lat1 + lat2) / 2)
            y = lat2 - lat1
            return round(EARTH_RADIUS * sqrt(x * x + y * y), 2)
        return None

    def new_calculate_distance(self, ref_lat, ref_lon):
        if self.latitude is not None and self.longitude is not None:
            lat1 = radians(ref_lat)
            lon1 = radians(ref_lon)
            lat2 = radians(self.latitude)
            lon2 = radians(self.longitude)
            dlat = lat1 - lat2
            dlon = lon1 - lon2
            sinlat = sin(dlat)
            sinlon = sin(dlong)
            cosone = cos(lat1)
            costwo = cos(lat2)
            aaaa = sinlat * sinlat + cosone * costwo * sinlon * sinlon
            cccc = asin(sqrt(aaaa))
            return round(EARTH_RADIUS * cccc * 2, 2)
        return None

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.fetch_location_data()
        self.distance = self.calculate_distance()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} at {self.address}"
    


    owner_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100) 

    @property
    def is_reserved(self):
        return self.reservations.filter(status='confirmed').exists()


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    reservation_id = models.AutoField(primary_key=True)
    accommodation = models.ForeignKey(
        Accommodation, related_name='reservations', on_delete=models.CASCADE
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 记录预约人
    start_date = models.DateField()  # 开始日期
    end_date = models.DateField()    # 结束日期

    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    rating = models.IntegerField(null=True, blank=True)  # Rating 0-5 after contract end
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    rating = models.IntegerField(null=True, blank=True)  # Rating 0-5 after contract end

    # def __str__(self):
    #     return f"{self.accommodation.address} — {self.status}"
    def __str__(self):
        return f"{self.accommodation.address} reserved by {self.user.email} from {self.start_date} to {self.end_date}"    

