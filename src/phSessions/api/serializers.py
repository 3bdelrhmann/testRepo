from phSessions.models import SessionReviews
from rest_framework  import serializers
from accounts.models import User


class SessionsReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SessionReviews
        fields = '__all__'
    