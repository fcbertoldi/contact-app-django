from django.forms import EmailInput, ModelForm
from django.urls import reverse

from contact_app_django.utils.htmx.forms import FormMixin

from .models import Contact


class ContactForm(FormMixin, ModelForm):
    class Meta:
        model = Contact
        fields = ["first", "last", "email", "phone"]
        widgets = {
            "email": EmailInput(
                attrs={
                    "hx-target": "next .form-field-error",
                    "hx-trigger": "change, keyup delay:200ms changed",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        if instance := kwargs.get("instance"):
            viewname = "core:validate-contact-email"
            viewname_kwargs = {"id": instance.id}
        else:
            viewname = "core:validate-new-email"
            viewname_kwargs = None

        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"hx-post": reverse(viewname, kwargs=viewname_kwargs)}
        )
