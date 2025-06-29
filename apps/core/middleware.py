from typing import Optional

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.utils.translation import gettext_lazy as _


class DjangoExceptionParserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Optional[HttpResponse]:
        response: HttpResponse = self.get_response(request)

        mapping = {
            404: _("Page not found"),
            405: _("Method not allowed"),
        }

        if isinstance(response, (HttpResponseNotFound, HttpResponseNotAllowed)):
            return JsonResponse(
                data={
                    "error": True,
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "details": {
                        "message": mapping.get(response.status_code, _("Unknown error"))
                    },
                },
                status=response.status_code,
            )

        return response
