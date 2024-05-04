from django.http import HttpResponse
from django.http.response import HttpResponseRedirectBase
from django.views import generic


class HttpResponseSeeOther(HttpResponseRedirectBase):
    status_code = 303


class HtmxDeletionMixin:
    redirect = True

    def should_redirect(self) -> bool:
        return self.redirect

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.

        The redirect, which is often done with 302, must be changed to 303 See Other, because the HTTP method
        must be GET, which is different from the request (DELETE).
        """
        self.object = self.get_object()
        self.object.delete()
        if self.should_redirect():
            return HttpResponseSeeOther(self.get_success_url())
        else:
            return HttpResponse()


class HtmxDeleteView(HtmxDeletionMixin, generic.DeleteView):
    pass
