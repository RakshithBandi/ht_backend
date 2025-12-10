from rest_framework import serializers
from .models import ChitFund

class ChitFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChitFund
        fields = '__all__'
