from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserForm


class SignUp(CreateView):
    form_class = UserForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
