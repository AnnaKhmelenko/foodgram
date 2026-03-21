from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from recipes.models import Recipe


class RecipeShortLinkRedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, short_code):
        try:
            recipe = Recipe.objects.get(short_code=short_code)
            return redirect(f'/recipes/{recipe.id}/')
        except Recipe.DoesNotExist:
            return redirect('/404')
