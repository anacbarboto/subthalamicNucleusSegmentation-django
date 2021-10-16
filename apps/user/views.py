import json

from django.contrib.auth import authenticate, get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .serializers import AuthUserSerializer

# Create your views here. (manejan la lógica)

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            serializer = AuthUserSerializer(user, context={'token':token.key})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """
    API endpoint for user login
    """
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


