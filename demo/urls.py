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


# from django.contrib import admin
# from django.urls import path, include  # include is required
# from orders import views 

# urlpatterns = [

# ]



# from django.contrib import admin
# from django.urls import path, include  # include is required
# from orders import views 

# urlpatterns = [

# ]



from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('orders.urls')),  
# ]

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('orders.urls')),

    # 这一行是关键，SwaggerView 和 RedocView 都依赖它
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Redoc 文档（可选）
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
