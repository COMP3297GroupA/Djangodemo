# orders/serializers.py

from rest_framework import serializers
from .models import Accommodation, Reservation


class AccommodationSerializer(serializers.ModelSerializer):
    is_reserved = serializers.ReadOnlyField()
    distance = serializers.FloatField(read_only=True)  # 添加这个

    class Meta:
        model = Accommodation
        fields = '__all__'


class ReservationRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField(help_text="Reservation start date (YYYY-MM-DD)")
    end_date = serializers.DateField(help_text="Reservation end date (YYYY-MM-DD)")

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data



class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=0, max_value=5)

    def validate_rating(self, value):
        if not 0 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value



class CancelReservationSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()



class ReservationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)


    class Meta:
        model = Reservation
        fields = '__all__'
        extra_kwargs = {
            'start_date': {'help_text': 'Reservation start date (YYYY-MM-DD)'},
            'end_date': {'help_text': 'Reservation end date (YYYY-MM-DD)'},
            'status': {'help_text': 'Reservation status: confirmed or cancelled'},
        }