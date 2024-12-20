from django.contrib.auth.mixins import LoginRequiredMixin

from kitchen.forms import PizzaSearchForm, PizzaTypeSearchForm
from kitchen.models import Pizza, PizzaType
from django.urls import reverse_lazy
from django.views import generic


class PizzaDetailView(generic.DetailView):
    model = Pizza
    template_name = "kitchen/pizza_detail.html"
    context_object_name = "pizza"


class PizzaCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pizza
    fields = ["name", "description", "pizza_type", "price", "pizzaioli"]
    template_name = "kitchen/pizza_form.html"
    success_url = reverse_lazy("kitchen:pizza-list")


class PizzaUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pizza
    fields = ["name", "description", "pizza_type", "price", "pizzaioli"]
    template_name = "kitchen/pizza_form.html"
    success_url = reverse_lazy("kitchen:pizza-list")


class PizzaDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Pizza
    template_name = "kitchen/pizza_confirm_delete.html"
    success_url = reverse_lazy("kitchen:pizza-list")


class PizzaListView(generic.ListView):
    model = Pizza
    template_name = "kitchen/pizza_list.html"
    context_object_name = "pizzas"
    queryset = Pizza.objects.all().prefetch_related("pizzaioli")
    paginate_by = 5

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PizzaSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = PizzaSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"])
        return self.queryset


class PizzaTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = PizzaType
    fields = ["name"]
    template_name = "kitchen/pizza_type_detail.html"
    success_url = reverse_lazy("kitchen:pizza-type-list")


class PizzaTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = PizzaType
    fields = ["name"]
    template_name = "kitchen/pizza_type_form.html"
    success_url = reverse_lazy("kitchen:pizza-type-list")


class PizzaTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = PizzaType
    template_name = "kitchen/pizza_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:pizza-type-list")

class PizzaTypeListView(generic.ListView):
    model = PizzaType
    template_name = "kitchen/pizza_type_list.html"
    context_object_name = "pizza_types"
    queryset = PizzaType.objects.all()
    paginate_by = 6

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PizzaTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PizzaTypeSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = PizzaType.objects.all()
        form = PizzaTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset

class HomePage(generic.TemplateView):
    template_name = "home.html"
