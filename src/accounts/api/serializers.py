from rest_framework import serializers
from accounts.models import Governorate,Region,User

class GovernorateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class LawyersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'