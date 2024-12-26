from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Person


def send_email(person: Person, subject: str, template: str, **kwargs):
    if not all(
        [
            isinstance(person, Person),
            isinstance(subject, str),
            isinstance(template, str),
        ],
    ):
        msg = "Invalid argument types. Expected (Person, str, str)"
        raise TypeError(msg)

    context = {"person": person, "name": person.get_short_name()}
    context.update(kwargs)

    message = render_to_string(template, context)
    send_mail(
        subject=subject,
        message=message,
        html_message=message,
        from_email=None,
        recipient_list=[person.email],
        fail_silently=False,
    )
