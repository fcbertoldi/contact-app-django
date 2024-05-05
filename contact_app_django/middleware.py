from django.http import QueryDict


class EnrichDeleteRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "DELETE":
            request.DELETE = QueryDict(request.body)
        response = self.get_response(request)
        return response
