from rest_framework import serializers

from api.serializers.recipe import Base64ImageField


class AvatarSerializer(serializers.Serializer):
    avatar = Base64ImageField()
