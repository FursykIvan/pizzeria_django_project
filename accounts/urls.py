from django.urls import include, path

from accounts.views import PizzaioloDetailView, activate, register, PizzaioloListView, PizzaioloUpdateView

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("activate/<str:uid>/<str:token>/", activate, name="activate"),
    path("profile/", PizzaioloDetailView.as_view(), name="profile"),
    path("pizzas/", PizzaioloListView.as_view(), name="pizzas"),
    path("profile/update/", PizzaioloUpdateView.as_view(), name="update_profile"),
]
