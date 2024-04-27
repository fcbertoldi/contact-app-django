from django.forms import ModelForm, EmailField
from .models import Contact


class ContactForm(ModelForm):
    email = EmailField()

    class Meta:
        model = Contact
        fields = ["first", "last", "email", "phone"]
