from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse
from django.views import generic, View
from contact_app_django.utils import HtmxDeleteView
from .forms import ContactForm
from .models import Contact


class IndexView(generic.ListView):
    model = Contact
    template_name = "index.html"
    context_object_name = "contacts"

    def get_queryset(self) -> QuerySet[Any]:
        search_param = self.request.GET.get("q") or None
        if search_param:
            return Contact.objects.search(search_param)

        return super().get_queryset()


class CreateContactView(generic.CreateView):
    model = Contact
    template_name = "contact_create.html"
    form_class = ContactForm

    def get_success_url(self) -> str:
        return reverse("core:contact-index")


class DetailContactView(generic.DetailView):
    model = Contact
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "contact_detail.html"


class EditContactView(generic.UpdateView):
    model = Contact
    slug_field = "id"
    slug_url_kwarg = "id"
    template_name = "contact_edit.html"
    form_class = ContactForm

    def get_success_url(self) -> str:
        return reverse("core:contact-index")


class DeleteContactView(HtmxDeleteView):
    model = Contact
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_success_url(self) -> str:
        return reverse("core:contact-index")


class ContactView(View):
    def get(self, request, *args, **kwargs):
        view = DetailContactView.as_view()
        return view(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        view = DeleteContactView.as_view()
        return view(request, *args, **kwargs)
