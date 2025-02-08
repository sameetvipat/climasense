from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),  # This ensures requests go to your 'weather' app
]
