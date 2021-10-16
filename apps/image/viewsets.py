from apps.image.serializers import ImageSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Image
from .serializers import ImageSerializer
from .principal import getSegmentation


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    
    @action(methods=['post'], detail=False)
    def segmentate(self, request):
    	t1 = request.data.get('t1')
    	t2 = request.data.get('t2')
    	
    	result_path = getSegmentation(t1, t2)
    	
    	result = Image()
    	result.type = 3
    	result.path = result_path
    	result.user = request.user
    	result.save()
    	
    	result_serializer = ImageSerializer(result)
    	
    	return Response(result_serializer.data, status=status.HTTP_201_CREATED)
