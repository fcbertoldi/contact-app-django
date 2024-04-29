from django.http.response import HttpResponseRedirectBase
from django.views import generic
from .form_renderers import HtmxFormMixin


class HttpResponseSeeOther(HttpResponseRedirectBase):
    status_code = 303


class HtmxDeletionMixin:
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.

        The redirect, which is often done with 302, must be changed to 303 See Other, because the HTTP method
        must be GET, which is different from the request (DELETE).
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseSeeOther(success_url)


class HtmxDeleteView(HtmxDeletionMixin, generic.DeleteView):
    pass


__all__ = [
    "HttpResponseSeeOther",
    "HtmxDeletionMixin",
    "HtmxDeleteView",
    "HtmxFormMixin",
]
