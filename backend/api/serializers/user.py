from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from users.models import User


class CurrentUserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(user=request.user).exists()


class UserSerializer(CurrentUserSerializer):
    pass
