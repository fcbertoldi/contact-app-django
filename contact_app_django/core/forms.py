from django.forms import ModelForm, EmailInput
from django.urls import reverse
from .models import Contact


class ContactForm(ModelForm):
    template_name = "contact_form.html"

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
        contact_id = kwargs.pop("id")
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"hx-post": reverse("core:validate-contact-email", args=[contact_id])}
        )
