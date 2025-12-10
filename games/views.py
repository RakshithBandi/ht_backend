from rest_framework import viewsets
from .models import Game
from .serializers import GameSerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
