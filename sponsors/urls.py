from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SponsorViewSet

router = DefaultRouter()
router.register(r'', SponsorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
