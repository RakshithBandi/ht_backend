from rest_framework import viewsets
from .models import ChitFund
from .serializers import ChitFundSerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class ChitFundViewSet(viewsets.ModelViewSet):
    queryset = ChitFund.objects.all()
    serializer_class = ChitFundSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
