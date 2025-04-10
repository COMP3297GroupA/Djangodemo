# # orders/views.py

# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Accommodation, Reservation
# from .serializers import AccommodationSerializer, ReservationSerializer
# from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend

# class AccommodationViewSet(viewsets.ModelViewSet):
#     queryset = Accommodation.objects.all()
#     serializer_class = AccommodationSerializer

#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_fields = ['type', 'period_of_availability', 'number_of_beds', 'number_of_bedrooms']
#     ordering_fields = ['price', 'distance']  # 可通过 ordering=price 排序

#     @action(detail=True, methods=['post'])
#     def reserve(self, request, pk=None):
#         accommodation = self.get_object()
#         if accommodation.is_reserved:
#             return Response({'error': 'Already reserved'}, status=400)

#         reservation = Reservation.objects.create(accommodation=accommodation)
#         serializer = ReservationSerializer(reservation)
#         return Response(serializer.data)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         try:
#             reservation = Reservation.objects.get(accommodation_id=pk, status='confirmed')
#             reservation.status = 'cancelled'
#             reservation.save()
#             return Response({'message': 'Reservation cancelled.'})
#         except Reservation.DoesNotExist:
#             return Response({'error': 'No active reservation.'}, status=404)




from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Accommodation, Reservation
from .serializers import AccommodationSerializer, ReservationSerializer

class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['type', 'period_of_availability', 'number_of_beds', 'number_of_bedrooms', 'price']
    ordering_fields = ['price', 'distance']
    search_fields = ['type', 'address']  # 增强搜索

    def get_queryset(self):
        queryset = Accommodation.objects.all()
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        accommodation = self.get_object()
        if accommodation.is_reserved:
            return Response({'error': 'Already reserved'}, status=400)

        reservation = Reservation.objects.create(accommodation=accommodation)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(accommodation_id=pk, status='confirmed')
            reservation.status = 'cancelled'
            reservation.save()
            return Response({'message': 'Reservation cancelled.'})
        except Reservation.DoesNotExist:
            return Response({'error': 'No active reservation.'}, status=404)


class ReservationViewSet(viewsets.ModelViewSet):  # 为 specialist 添加
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

