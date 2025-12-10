from rest_framework import viewsets
from .models import Sponsor
from .serializers import SponsorSerializer
from api.permissions import IsAdminOrManagerOrReadOnly

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: User: {request.user}")
        print(f"DEBUG: User groups: {list(request.user.groups.values_list('name', flat=True)) if request.user.is_authenticated else 'N/A'}")
        return super().create(request, *args, **kwargs)
