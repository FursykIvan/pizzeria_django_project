from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic

from accounts.forms import RegisterForm
from accounts.models import Pizzaiolo
from accounts.services.email_service import EmailService
from accounts.services.token_service import account_activation_token


User = get_user_model()


def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            email_service = EmailService()
            email_service.send_activation_email(
                username=user.username,
                domain=domain,
                uid=uid,
                to_email=user.email,
                token=token,
            )

            messages.info(request, "Please confirm your activation")

            return redirect("accounts:login")

    return render(request, "accounts/register.html", {"form": form})


def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user.is_active:
        return HttpResponse("Your account is already activated")

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")


class PizzaioloDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = "accounts/profile.html"
    context_object_name = "user"


class PizzaioloUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pizzaiolo
    fields = ["username", "email", "year_of_experience"]
    template_name = "accounts/update_profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user


class PizzaioloListView(LoginRequiredMixin, generic.ListView):
    model = Pizzaiolo
    template_name = "accounts/pizzaiolos_list.html"

    def get_queryset(self):
        return Pizzaiolo.objects.all().prefetch_related("pizzas")
