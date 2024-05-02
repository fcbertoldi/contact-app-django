from typing import Any
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import generic, View
from django.views.decorators.http import require_http_methods
from contact_app_django.utils import HtmxDeleteView
from .forms import ContactForm
from .models import Contact


class IndexView(generic.ListView):
    model = Contact
    context_object_name = "contacts"
    ordering = ["created_at", "first", "last"]
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        search_param = self.request.GET.get("q") or None
        if search_param:
            return Contact.objects.search(search_param)

        return super().get_queryset()

    def get_template_names(self) -> list[str]:
        if self.request.htmx and self.request.htmx.trigger == "search":
            return ["rows.html"]
        else:
            return ["index.html"]


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


@require_http_methods(["POST"])
def validate_email_view_alt(request: HttpRequest, id):
    email = request.POST.get("email")
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponse("Invalid email")

    if Contact.objects.exclude(id=id).filter(email=email).exists():
        return HttpResponse("Email already exists")

    return HttpResponse()


@require_http_methods(["POST"])
def validate_email_view(request: HttpRequest, id=None):
    contact = None
    if id is not None:
        contact = get_object_or_404(Contact, pk=id)

    form = ContactForm(data=request.POST, instance=contact)
    if not form.is_valid() and "email" in form.errors:
        return HttpResponse(form.errors["email"])

    return HttpResponse()
