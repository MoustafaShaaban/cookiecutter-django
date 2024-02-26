import datetime
{%- if cookiecutter.username_type == "email" %}
from typing import ClassVar
{% endif -%}
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField, ImageField
{%- if cookiecutter.username_type == "email" %}
from django.db.models import EmailField
{%- endif %}
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
{%- if cookiecutter.username_type == "email" %}

from .managers import UserManager
{%- endif %}


class User(AbstractUser):
    """
    Default custom user model for {{cookiecutter.project_name}}.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    date_of_birth = DateField(_("User Date of Birth"), blank=True, default=datetime.date.today)
    avatar = ImageField(_("User Avatar"), upload_to="users_avatar", default="default.jpg")
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    {%- if cookiecutter.username_type == "email" %}
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
    {%- endif %}

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        {%- if cookiecutter.username_type == "email" %}
        return reverse("users:detail", kwargs={"pk": self.id})
        {%- else %}
        return reverse("users:detail", kwargs={"username": self.username})
        {%- endif %}
