from django.shortcuts import get_object_or_404, redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from recipes.models import Recipe


class RecipeShortLinkRedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, short_code):
        recipe = get_object_or_404(Recipe, short_code=short_code)
        return redirect(f'/recipes/{recipe.id}/')
