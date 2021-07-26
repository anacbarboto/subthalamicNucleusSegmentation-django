from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Profile


User = get_user_model()


class AuthUserSerializer(ModelSerializer):
    token = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'token')
    
    def get_token(self, obj):
        return self.context.get('token', '')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'entity', 'role')
    

class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'email', 'profile')


class UserListSerializer(ModelSerializer):
    role = SerializerMethodField()
    entity = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'role', 'entity')

    def get_role(self, user):
        return user.profile.role
    
    def get_entity(self, user):
        return user.profile.entity