from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Expenditure
from .serializers import ExpenditureSerializer

from api.permissions import IsAdminOrManagerOrReadOnly


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ExpenditureViewSet(viewsets.ModelViewSet):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [IsAdminOrManagerOrReadOnly]
