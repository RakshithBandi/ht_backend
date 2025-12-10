from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Announcement
from .serializers import AnnouncementSerializer
from api.permissions import IsAdminOrManagerOrReadOnly
from members.models import PermanentMember, TemporaryMember, JuniorMember
from sponsors.models import Sponsor
from games.models import Game

class DashboardStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        permanent_members_count = PermanentMember.objects.count()
        temporary_members_count = TemporaryMember.objects.count()
        junior_members_count = JuniorMember.objects.count()
        sponsors_count = Sponsor.objects.count()
        
        # Calculate winners count (games with a winnerName)
        winners_count = Game.objects.exclude(winnerName__isnull=True).exclude(winnerName__exact='').count()

        data = {
            'permanentMembers': permanent_members_count,
            'temporaryMembers': temporary_members_count,
            'juniorMembers': junior_members_count,
            'sponsors': sponsors_count,
            'winners': winners_count,
        }
        return Response(data)

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]
    
    def perform_create(self, serializer):
        # Save the announcement
        announcement = serializer.save()
        
        # Create notifications for all users
        from notifications.models import Notification
        users = User.objects.all()
        
        notifications_to_create = [
            Notification(
                user=user,
                announcement=announcement,
                title=f"New Announcement: {announcement.heading}",
                body=announcement.description[:200]  # Limit to 200 chars
            )
            for user in users
        ]
        
        Notification.objects.bulk_create(notifications_to_create)

