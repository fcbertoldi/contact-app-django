from django.forms import ModelForm, EmailInput
from django.urls import reverse
from contact_app_django.utils import HtmxFormMixin
from .models import Contact


class ContactForm(HtmxFormMixin, ModelForm):
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
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "hx-post": reverse(
                    "core:validate-contact-email", kwargs={"id": self.instance.id}
                )
            }
        )
