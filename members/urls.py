from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PermanentMemberViewSet, TemporaryMemberViewSet, JuniorMemberViewSet

router = DefaultRouter()
router.register(r'permanent', PermanentMemberViewSet)
router.register(r'temporary', TemporaryMemberViewSet)
router.register(r'junior', JuniorMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
