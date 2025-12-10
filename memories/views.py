from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Memory
from .serializers import MemorySerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAdminOrManagerOrReadOnly]
