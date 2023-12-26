from rest_framework import HTTP_HEADER_ENCODING
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomHeaderJWTAuthentication(JWTAuthentication):
    def get_header(self, request) -> bytes:
        header = "Authorize"

        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)

        return header
