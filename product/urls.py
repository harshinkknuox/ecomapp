from django.urls import path
from .api import ProductViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    path('products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
]