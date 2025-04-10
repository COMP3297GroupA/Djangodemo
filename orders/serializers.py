# orders/serializers.py

from rest_framework import serializers
from .models import Accommodation, Reservation


class AccommodationSerializer(serializers.ModelSerializer):
    is_reserved = serializers.ReadOnlyField()

    class Meta:
        model = Accommodation
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'