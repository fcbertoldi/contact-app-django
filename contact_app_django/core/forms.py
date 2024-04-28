from django.forms import ModelForm
from .models import Contact


class ContactForm(ModelForm):
    template_name = "contact_form.html"

    class Meta:
        model = Contact
        fields = ["first", "last", "email", "phone"]
