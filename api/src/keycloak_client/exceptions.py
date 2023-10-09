from rest_framework import status
from rest_framework.exceptions import APIException


class AppUnauthorizedException(APIException):
    """
    App generic unauthorized exception.
    """

    def __init__(self, detail):
        super().__init__(detail)
        self.status_code = status.HTTP_401_UNAUTHORIZED

    def __str__(self):
        return f"[{self.status_code}] {self.detail}"
