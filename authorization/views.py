from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authorization.forms import RegisterUserForm, LoginForm


class MySignupView(CreateView):
    model = User
    form_class = RegisterUserForm
    success_url = reverse_lazy('main_view')
    template_name = 'findjob/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'findjob/login.html'
    redirect_authenticated_user = True


def logout_user(request):
    logout(request)
    return redirect('/')

