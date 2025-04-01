from django.urls import path
from . import views

urlpatterns = [
    path('accommodations/', views.browse_accommodations, name='browse_accommodations'),
    path('accommodations/<int:accommodation_id>/', views.accommodation_detail, name='accommodation_detail'),
    path('accommodations/<int:accommodation_id>/reserve/', views.reserve_accommodation, name='reserve_accommodation'),
]