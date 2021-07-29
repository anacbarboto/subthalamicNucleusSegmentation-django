from rest_framework.serializers import ModelSerializer

from .models import Model


class ModelSerializer(ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'user', 'path', 'is_active')
    