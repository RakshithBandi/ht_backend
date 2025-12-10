from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    profilePicture = serializers.CharField(source='profile_picture', required=False, allow_blank=True)
    
    class Meta:
        model = UserProfile
        fields = ['fullName', 'email', 'username', 'phone', 'profilePicture']
    
    def get_fullName(self, obj):
        first_name = obj.user.first_name or ''
        last_name = obj.user.last_name or ''
        full_name = f"{first_name} {last_name}".strip()
        return full_name if full_name else obj.user.username
    
    def update(self, instance, validated_data):
        # Update phone and profile picture
        instance.phone = validated_data.get('phone', instance.phone)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        
        # Update user's first and last name if fullName is provided
        full_name = self.initial_data.get('fullName', '')
        if full_name:
            name_parts = full_name.split(' ', 1)
            instance.user.first_name = name_parts[0]
            instance.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            instance.user.save()
        
        return instance
