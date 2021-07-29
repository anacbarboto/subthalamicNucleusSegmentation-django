from django.urls import path, include

from rest_framework import routers

from .viewsets import ModelViewSet


router = routers.DefaultRouter()
router.register(r'models', ModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
