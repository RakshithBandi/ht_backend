from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'heading', 'year', 'description', 'created_at']
        read_only_fields = ['created_at']
