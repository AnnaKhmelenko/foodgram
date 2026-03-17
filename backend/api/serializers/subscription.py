from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.serializers.recipe import (
    RecipeAuthorSerializer,
    RecipeShortSerializer
)

User = get_user_model()


class SubscriptionSerializer(RecipeAuthorSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(RecipeAuthorSerializer.Meta):
        model = User
        fields = RecipeAuthorSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()

        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            try:
                recipes = recipes[:int(recipes_limit)]
            except ValueError:
                pass

        return RecipeShortSerializer(
            recipes,
            many=True,
            context=self.context
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
