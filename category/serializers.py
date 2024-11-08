from rest_framework import serializers

from .models import ProductCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','slug','title', 'cate_title']