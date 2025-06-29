from typing import Any, Optional

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class CustomAPIException(APIException):
    default_code = "ERROR"
    default_detail = {"message": _("An internal server error occurred.")}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        code: Optional[str],
        detail: Optional[dict[str, Any]],
        status_code: Optional[int],
    ):
        self.default_code = code if code else self.default_code
        self.default_detail = detail if detail else self.default_detail
        self.status_code = status_code if status_code else self.status_code

        super().__init__(
            code=self.default_code,
            detail=self.default_detail,
        )


def handler(exc: Exception | CustomAPIException, context: Optional[dict[str, Any]]):

    response: Optional[Response] = drf_exception_handler(exc, context)
    request: Optional[Request] = context.get("request", None)

    method: str = request.method if request else "Unknown"
    path: str = request.path if request else "Unknown"

    if response is not None:
        if isinstance(exc, APIException):
            if isinstance(exc, CustomAPIException):
                return Response(
                    data={
                        "error": True,
                        "method": method,
                        "path": path,
                        "status_code": exc.status_code,
                        "details": exc.default_detail,
                    },
                    status=exc.status_code,
                )

            return Response(
                data={
                    "error": True,
                    "method": method,
                    "path": path,
                    "status_code": exc.status_code,
                    "details": exc.default_detail,
                },
                status=exc.status_code,
            )

    return Response(
        data={
            "error": True,
            "method": method,
            "path": path,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "details": exc.default_detail,
        },
        status=exc.status_code,
    )
