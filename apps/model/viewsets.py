from apps.model.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Model
from .serializers import ModelSerializer


User = get_user_model() 

def deactivate_all_models():
    	active_models = Model.objects.filter(is_active=True)
    	
    	if (len(active_models) > 0):
    		last_active_model = Model.objects.filter(is_active=True).first()
    		last_active_model.is_active = False
    		last_active_model.save()

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    
    def create(self, request):
        try:
            user = request.data.get('user', 0)
            u = get_object_or_404(User, pk=user)
            path = request.FILES['path']
            print(path)
            is_active = request.data.get('is_active', True)

            deactivate_all_models()

            model = Model()
            model.user = u
            model.path = path
            model.is_active = is_active
            model.save()

            serializer = ModelSerializer(model)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
    	
    	deactivate_all_models()
    	
    	model = get_object_or_404(Model, pk=pk)
    	model.is_active = True
    	model.save()
    	
    	return Response(status=status.HTTP_204_NO_CONTENT)
