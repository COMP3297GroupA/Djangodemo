# from django.urls import path
# from . import views

# urlpatterns = [

# ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccommodationViewSet , ReservationViewSet

router = DefaultRouter()
router.register(r'accommodations', AccommodationViewSet)
router.register(r'reservations', ReservationViewSet) 

urlpatterns = [
    path('', include(router.urls)),
]