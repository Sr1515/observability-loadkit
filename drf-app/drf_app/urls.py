from django.contrib import admin
from django.urls import path, include
from products.views import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('health/', health),
    path('', include('django_prometheus.urls')),

]
