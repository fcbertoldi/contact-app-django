from django.shortcuts import render
from django.views import generic
from .models import Contact


class IndexView(generic.ListView):
    template_name = "index.html"
    queryset = Contact.objects.all()
    context_object_name = "contacts"
