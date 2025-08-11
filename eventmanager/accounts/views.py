from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserRegisterForm


class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('event-list')  # Redirect after success

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the newly registered user
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'