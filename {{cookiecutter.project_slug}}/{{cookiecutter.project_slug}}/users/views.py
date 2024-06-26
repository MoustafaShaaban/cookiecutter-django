from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from {{ cookiecutter.project_slug }}.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    {%- if cookiecutter.username_type == "email" %}
    slug_field = "id"
    slug_url_kwarg = "id"
    {%- else %}
    slug_field = "username"
    slug_url_kwarg = "username"
    {%- endif %}


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name", "avatar"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        {%- if cookiecutter.username_type == "email" %}
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})
        {%- else %}
        return reverse("users:detail", kwargs={"username": self.request.user.username})
        {%- endif %}


user_redirect_view = UserRedirectView.as_view()
