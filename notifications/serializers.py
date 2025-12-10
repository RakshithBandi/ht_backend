from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    isNew = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'body', 'timestamp', 'is_read', 'isNew', 'announcement']
        read_only_fields = ['timestamp']
    
    def get_isNew(self, obj):
        return not obj.is_read
