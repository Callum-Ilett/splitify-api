"""Views for the auth0authorization app."""

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def public(_request: HttpRequest) -> JsonResponse:
    """Return response from public endpoint."""
    return JsonResponse({"message": "This is a public endpoint!"})


@api_view(["GET"])
def private(_request: HttpRequest) -> JsonResponse:
    """Return response from private endpoint."""
    return JsonResponse({"message": "This is a private endpoint!"})
