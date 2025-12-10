from rest_framework import serializers
from .models import PermanentMember, TemporaryMember, JuniorMember

class PermanentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentMember
        fields = '__all__'

class TemporaryMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryMember
        fields = '__all__'

class JuniorMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = JuniorMember
        fields = '__all__'
