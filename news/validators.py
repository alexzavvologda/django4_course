from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def russian_email(email):
    allowed_domains = ['@mail.ru', '@rambler.ru', '@yandex.ru']
    if not (any(domain in email for domain in allowed_domains)):
        raise ValidationError(
            _("%(emails) has not allowed domain"),
            params={"email": email},
        )
