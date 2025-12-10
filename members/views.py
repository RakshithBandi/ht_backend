from rest_framework import viewsets
from .models import PermanentMember, TemporaryMember, JuniorMember
from .serializers import PermanentMemberSerializer, TemporaryMemberSerializer, JuniorMemberSerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class PermanentMemberViewSet(viewsets.ModelViewSet):
    queryset = PermanentMember.objects.all()
    serializer_class = PermanentMemberSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]

class TemporaryMemberViewSet(viewsets.ModelViewSet):
    queryset = TemporaryMember.objects.all()
    serializer_class = TemporaryMemberSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]

class JuniorMemberViewSet(viewsets.ModelViewSet):
    queryset = JuniorMember.objects.all()
    serializer_class = JuniorMemberSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
