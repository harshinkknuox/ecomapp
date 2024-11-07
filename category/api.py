from rest_framework.response import Response
from rest_framework import viewsets,status
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language_from_request
from .models import ProductCategory
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    def get_serializer_class(self):
        group_serializer = {
            'list':CategorySerializer
        }
        if self.action in group_serializer.keys():
            return group_serializer[self.action]

    def list(self,request,*args,**kwargs):
        response = {}
        try :
            querysets = ProductCategory.objects.all()
            records= querysets
            serializer = self.get_serializer(records,many=True,context={'request':request})
            response['result'] = 'success'
            response['records'] = serializer.data
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)
        return Response(response, status=status.HTTP_200_OK)