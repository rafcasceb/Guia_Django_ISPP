from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet


router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename="hotels")  # las reverse urls se obtienen con "{basename}-{url_name}"

urlpatterns = [
    path('api/', include(router.urls)),
]
