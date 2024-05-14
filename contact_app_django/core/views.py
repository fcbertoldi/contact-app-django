import random
from http import HTTPStatus
from time import sleep
from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View, generic
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event

from contact_app_django.utils import HtmxDeleteView

from .forms import ContactForm
from .models import Contact
from .services import ArchiverException, archiver


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

    def search_triggered(self) -> bool:
        return self.request.htmx and self.request.htmx.trigger == "search"

    def get_template_names(self) -> list[str]:
        return ["rows.html"] if self.search_triggered() else ["index.html"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "contact_count": Contact.objects.count(),
            }
        )
        if not self.search_triggered():
            context.update(
                {
                    "archiver_status": archiver.status.name,
                }
            )

        return context

    def delete(self, request):
        contact_ids = request.DELETE.getlist("selected_contact_ids")
        num_deleted, _ = Contact.objects.filter(id__in=contact_ids).delete()
        response = self.get(request)
        if num_deleted > 0:
            archiver.reset()
            response = trigger_client_event(response, "contactsUpdated")

        return response


class CreateContactView(generic.CreateView):
    model = Contact
    template_name = "contact_create.html"
    form_class = ContactForm

    def get_success_url(self) -> str:
        return reverse("core:contact-index")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        archiver.reset()
        return trigger_client_event(response, "contactsUpdated")


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

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        archiver.reset()
        return trigger_client_event(response, "contactsUpdated")


class DeleteContactView(HtmxDeleteView):
    model = Contact
    slug_field = "id"
    slug_url_kwarg = "id"
    redirect_map = {
        "contact-delete-btn": True,
    }

    def get_success_url(self) -> str:
        return reverse("core:contact-index")

    def should_redirect(self) -> bool:
        if not self.request.htmx:
            return True

        redirect_element = self.redirect_map.get(self.request.htmx.trigger, False)
        return redirect_element

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return trigger_client_event(response, "contactsUpdated")


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


@require_http_methods(["GET"])
def slow_contact_count(request: HttpRequest):
    sleep(random.randrange(1, 3))  # nosec B311
    count = Contact.objects.count()
    return HttpResponse(f"({count} total contacts)")


class ArchiveMixin:
    template_name = "archive_ui.html"

    def get_context_data(self):
        return {
            "archiver_status": archiver.status.name,
            "archiver_progress": round(archiver.progress * 100),
        }


class ArchiveView(ArchiveMixin, View):
    def post(self, request, *args, **kwargs):
        archiver.archive()
        return render(
            request,
            template_name=self.template_name,
            context=self.get_context_data(),
            status=HTTPStatus.CREATED,
        )

    def get(self, request, *args, **kwargs):
        return render(
            request,
            template_name=self.template_name,
            context=self.get_context_data(),
        )


@require_http_methods(["GET"])
def archive_file(request: HttpRequest):
    try:
        return FileResponse(
            archiver.get_archive_file(), as_attachment=True, filename="contacts.json"
        )
    except ArchiverException as e:
        print(f"Error: {e}")
        return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED)


class ArchiveResetView(ArchiveMixin, View):
    def post(self, request, *args, **kwargs):
        archiver.reset()
        return render(
            request,
            template_name=self.template_name,
            context=self.get_context_data(),
        )
