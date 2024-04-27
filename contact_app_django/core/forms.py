from django.forms import ModelForm, EmailField
from .models import Contact


class ContactForm(ModelForm):
    template_name = "contact_form.html"

    email = EmailField()

    class Meta:
        model = Contact
        fields = ["first", "last", "email", "phone"]
