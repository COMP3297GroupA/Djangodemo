
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from .models import Accommodation, Reservation
from .serializers import AccommodationSerializer, ReservationSerializer, ReservationRequestSerializer, RatingSerializer
from datetime import datetime
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema


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
    

    @extend_schema(
        request=ReservationRequestSerializer,  # 告诉 Swagger 请求体结构
        responses=ReservationSerializer        # 告诉 Swagger 返回值结构
    )    

    @action(detail=True, methods=['post'], url_path='reserve', url_name='accommodations_reserve')
    def reserve(self, request, pk=None):
        accommodation = self.get_object()
        user = request.user  # 当前用户，确保你开启了认证
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")



        serializer = ReservationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']        

        # 检查是否有冲突
        overlapping = Reservation.objects.filter(
            accommodation=accommodation,
            status='confirmed',
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if overlapping.exists():
            return Response({'error': 'This time slot is already reserved.'}, status=400)

        # 创建预约
        reservation = Reservation.objects.create(
            accommodation=accommodation,
            user=user,
            start_date=start_date,
            end_date=end_date,
            # status='confirmed'
        )

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
        

        
    @action(detail=True, methods=['get'])              
    def reserved_periods(self, request, pk=None):        #  展示已被预约的时间段
        accommodation = self.get_object()
        reservations = accommodation.reservations.filter(status='confirmed').values('start_date', 'end_date')
        return Response(list(reservations))



class ReservationFilter(django_filters.FilterSet):    # 查询某个 accommodation 在某个日期范围内是否被预订
    start = django_filters.DateFilter(field_name="end_date", lookup_expr='gte')
    end = django_filters.DateFilter(field_name="start_date", lookup_expr='lte')

    class Meta:
        model = Reservation
        fields = ['accommodation', 'start', 'end']





class ReservationViewSet(viewsets.ModelViewSet):  # 为 specialist 添加
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter


    @extend_schema(
        request=RatingSerializer,
        responses={200: ReservationSerializer}
    )
    @action(detail=True, methods=['post'], url_path='rate')     # 评分功能，只有在reservation end time 之后才能进行评分
    def rate(self, request, pk=None):
        try:
            reservation = self.get_object()
            if reservation.user != request.user:
                return Response({'error': 'You can only rate your own reservations.'}, status=403)

            if reservation.end_date > datetime.today().date():
                return Response({'error': 'You can only rate after the end of the stay.'}, status=400)

            if reservation.rating is not None:
                return Response({'error': 'You have already rated this reservation.'}, status=400)

            serializer = RatingSerializer(data=request.data)
            if serializer.is_valid():
                reservation.rating = serializer.validated_data['rating']
                reservation.save()
                return Response(ReservationSerializer(reservation).data)
            return Response(serializer.errors, status=400)

        except Reservation.DoesNotExist:
            return Response({'error': 'Reservation not found.'}, status=404) 
