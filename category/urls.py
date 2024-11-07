from django.urls import path
from .api import CategoryViewSet

urlpatterns = [
    path('category/', CategoryViewSet.as_view({'get': 'list'}), name='product-list'),  
]