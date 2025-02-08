from django.urls import path
from .views import index  # ✅ Import the index view from views.py

urlpatterns = [
    path('', index, name='index'),  # Main route for the homepage
]
