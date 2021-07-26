from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserListSerializer
from .models import Profile
from segmentation.permissions import IsAdmin


User = get_user_model()


#hacen la vida facil, definen las respuestas de los http
#le dice a django que serializer usar
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'list': UserListSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes [self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        try:
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            username = request.data.get('username', '')
            email = request.data.get('email', '')
            phone = request.data.get('phone', '')
            entity = request.data.get('entity', '')
            role = request.data.get('role', '')

            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }

            user = User.objects.create_user(username, **user_data)
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.entity = entity
            profile.role = role
            profile.save()

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.profile.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

