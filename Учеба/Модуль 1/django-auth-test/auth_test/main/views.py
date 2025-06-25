from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import CustomUserCreationForm


class IndexView(TemplateView):
    template_name = 'index.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = reverse_lazy('login')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())
