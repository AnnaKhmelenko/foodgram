from django.urls import path
from .views import RecipeShortLinkRedirectView

urlpatterns = [
    path('s/<str:short_code>/', RecipeShortLinkRedirectView.as_view()),
]
