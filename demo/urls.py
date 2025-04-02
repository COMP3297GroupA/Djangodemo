"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include  # include is required
from orders import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_member, name='login'),  # ✅ 默认首页就是登录页
    path('logout/', views.logout_member, name='logout'),
    path('accommodations/', views.browse_accommodations, name='browse_accommodations'),
    path('accommodations/<str:address>/', views.accommodation_detail, name='accommodation_detail'),
    path('accommodations/<str:address>/reserve/', views.reserve_accommodation, name='reserve_accommodation'),
    # path('', include('orders.urls')),  # 👈 this line connects your app's URLs
]