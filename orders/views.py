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


<<<<<<< HEAD
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Accommodation, Reservation
from .serializers import AccommodationSerializer, ReservationSerializer
=======
# 1. Browse + Filter + Sort accommodations
def browse_accommodations(request):

    accommodations = Accommodation.objects.all()

    acc_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_distance = request.GET.get('min_distance')
    max_distance = request.GET.get('max_distance')
    sort_by = request.GET.get('sort_by')

    # 只有在参数不为空时才进行过滤
    if acc_type and acc_type.strip() != "":
        accommodations = accommodations.filter(type__icontains=acc_type)
    if min_price and min_price.strip() != "":
        accommodations = accommodations.filter(price__gte=min_price)
    if max_price and max_price.strip() != "":
        accommodations = accommodations.filter(price__lte=max_price)

    if min_distance and min_distance.strip() != "":
        accommodations = accommodations.filter(distance__gte=min_distance)
    if max_distance and max_distance.strip() != "":
        accommodations = accommodations.filter(distance__lte=max_distance)

    # 排序逻辑
    if sort_by == 'price':
        accommodations = accommodations.order_by('price')
    elif sort_by == 'distance':
        accommodations = accommodations.order_by('distance')

    #  accommodation 是否已预订
    for acc in accommodations:
        acc.is_reserved = acc.reservations.filter(status='confirmed').exists()

    return render(request, 'browse.html', {
        'accommodations': accommodations,
            'filters': {
                'type': acc_type or '',
                'min_price': min_price or '',
                'max_price': max_price or '',
                'min_distance': min_distance or '',
                'max_distance': max_distance or '',
                'sort_by': sort_by or '',
            }
    })
>>>>>>> c322db106e17935c56c39b3bfd6d927cceccdd19


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


<<<<<<< HEAD
class ReservationViewSet(viewsets.ModelViewSet):  # 为 specialist 添加
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
=======
        messages.success(request, "Accommodation added successfully.")
        return redirect('owner_dashboard')

    return render(request, 'add_accommodation.html')
>>>>>>> c322db106e17935c56c39b3bfd6d927cceccdd19
