from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from .forms import UserRegisterForm


class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')  # Redirect after success

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the newly registered user
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'


User = get_user_model()


class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/user-profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        # Return the current logged-in user
        return self.request.user