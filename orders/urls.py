from django.urls import path
from . import views

urlpatterns = [
    path('accommodations/', views.browse_accommodations, name='browse_accommodations'),
    path('accommodations/<str:address>/', views.accommodation_detail, name='accommodation_detail'),
    path('accommodations/<str:address>/reserve/', views.reserve_accommodation, name='reserve_accommodation'),
    path('owner/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/add/', views.add_accommodation, name='add_accommodation'),
]