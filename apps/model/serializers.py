from rest_framework.serializers import ModelSerializer

from .models import Model
from apps.user.serializers import UserSerializer

class ModelSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Model
        fields = ('id', 'user', 'path', 'is_active')
    
