from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    AvatarSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeShortSerializer,
    RecipeWriteSerializer,
    SubscriptionSerializer,
    TagSerializer,
    UserSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscription, User


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def _create_user_recipe_relation(self, model, request, pk=None):
        recipe = self.get_object()

        if model.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        model.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeShortSerializer(
            recipe,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_user_recipe_relation(self, model, request, pk=None):
        recipe = self.get_object()
        relation = model.objects.filter(user=request.user, recipe=recipe)

        if not relation.exists():
            return Response(
                {'errors': 'Рецепт не найден.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self._create_user_recipe_relation(Favorite, request, pk)
        return self._delete_user_recipe_relation(Favorite, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self._create_user_recipe_relation(ShoppingCart, request, pk)
        return self._delete_user_recipe_relation(ShoppingCart, request, pk)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__in_carts__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name')
        )

        lines = ['Список покупок:\n']
        for item in ingredients:
            lines.append(
                f"{item['ingredient__name']} "
                f"({item['ingredient__measurement_unit']}) — "
                f"{item['total_amount']}"
            )

        content = '\n'.join(lines)
        response = HttpResponse(
            content,
            content_type='text/plain; charset=utf-8',
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = request.build_absolute_uri(f'/s/{recipe.short_code}/')
        return Response(
            {'short-link': short_link},
            status=status.HTTP_200_OK,
        )


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        authors = User.objects.filter(subscribers__user=request.user)
        page = self.paginate_queryset(authors)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        author = self.get_object()

        if request.user == author:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == 'POST':
            if Subscription.objects.filter(
                user=request.user,
                author=author,
            ).exists():
                return Response(
                    {'errors': 'Вы уже подписаны.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Subscription.objects.create(user=request.user, author=author)
            serializer = SubscriptionSerializer(
                author,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscription = Subscription.objects.filter(
            user=request.user,
            author=author,
        )
        if not subscription.exists():
            return Response(
                {'errors': 'Подписка не найдена.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['put', 'delete'],
        permission_classes=[IsAuthenticated],
        url_path='me/avatar',
    )
    def avatar(self, request):
        if request.method == 'PUT':
            serializer = AvatarSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            request.user.avatar = serializer.validated_data['avatar']
            request.user.save()

            return Response(
                {'avatar': request.build_absolute_uri(
                    request.user.avatar.url)},
                status=status.HTTP_200_OK,
            )

        if request.user.avatar:
            request.user.avatar.delete(save=False)
            request.user.avatar = None
            request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeShortLinkRedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, short_code):
        recipe = get_object_or_404(Recipe, short_code=short_code)
        return redirect(f'/recipes/{recipe.id}/')
