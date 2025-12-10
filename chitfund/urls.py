from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChitFundViewSet

router = DefaultRouter()
router.register(r'', ChitFundViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
