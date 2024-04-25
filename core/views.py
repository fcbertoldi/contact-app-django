from typing import Any
from django.db.models.query import QuerySet
from django.views import generic
from .models import Contact

# TODO: pytest
# TODO: ruff
# TODO: detail
# TODO: create
# TODO: edit
# TODO: delete
# TODO: mudar cookiecutter pro django 4.2


class IndexView(generic.ListView):
    model = Contact
    template_name = "index.html"
    context_object_name = "contacts"

    def get_queryset(self) -> QuerySet[Any]:
        search_param = self.request.GET.get("q") or None
        if search_param:
            return Contact.objects.search(search_param)

        return super().get_queryset()
