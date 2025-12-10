from rest_framework import serializers
from .models import Question, UserResponse, UserScore, QuizSettings

class QuestionSerializer(serializers.ModelSerializer):
    already_answered = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    expires_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')

    def get_already_answered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserResponse.objects.filter(user=request.user, question=obj).exists()
        return False

    def get_expires_at(self, obj):
        from django.utils import timezone
        import datetime
        expiration_time = obj.created_at + datetime.timedelta(minutes=30)
        return expiration_time

    def get_is_expired(self, obj):
        from django.utils import timezone
        import datetime
        expiration_time = obj.created_at + datetime.timedelta(minutes=30)
        return timezone.now() > expiration_time

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = '__all__'
        read_only_fields = ('user', 'is_correct', 'answered_at')

class UserScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserScore
        fields = ('username', 'total_points')

class QuizSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSettings
        fields = ['is_leaderboard_visible']
