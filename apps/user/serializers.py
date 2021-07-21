from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer, SerializerMethodField


User = get_user_model()


class AuthUserSerializer(ModelSerializer):
    token = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'token')
    
    def get_token(self, obj):
        return self.context.get('token', '')
