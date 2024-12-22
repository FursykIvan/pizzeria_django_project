from django.urls import path

from kitchen.views import (
    HomePage,
    PizzaListView,
    PizzaCreateView,
    PizzaDetailView,
    PizzaUpdateView,
    PizzaDeleteView,
    PizzaTypeListView,
    PizzaTypeDetailView,
    PizzaTypeCreateView,
    PizzaTypeUpdateView,
    PizzaTypeDeleteView,
)

app_name = "kitchen"

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("pizza/", PizzaListView.as_view(), name="pizza-list"),
    path("pizza/create/", PizzaCreateView.as_view(), name="pizza-create"),
    path("pizza/<int:pk>/detail/", PizzaDetailView.as_view(), name="pizza-detail"),
    path("pizza/<int:pk>/update/", PizzaUpdateView.as_view(), name="pizza-update"),
    path("pizza/<int:pk>/delete/", PizzaDeleteView.as_view(), name="pizza-delete"),
    path("pizza_type/", PizzaTypeListView.as_view(), name="pizza-type-list"),
    path("pizza_type/<int:pk>/detail/", PizzaTypeDetailView.as_view(), name="pizza-type-detail"),
    path("pizza_type/create/", PizzaTypeCreateView.as_view(), name="pizza-type-create"),
    path("pizza_type/<int:pk>/update/", PizzaTypeUpdateView.as_view(), name="pizza-type-update"),
    path("pizza_type/<int:pk>/delete/", PizzaTypeDeleteView.as_view(), name="pizza-type-delete"),
]
