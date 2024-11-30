"""Views for the auth0authorization app."""

from django.http import HttpRequest, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def public(_request: HttpRequest) -> JsonResponse:
    """Return response from public endpoint."""
    message = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return JsonResponse({"message": message})


@api_view(["GET"])
def private(_request: HttpRequest) -> JsonResponse:
    """Return response from private endpoint."""
    message = "Hello from a private endpoint! You need to be authenticated to see this."
    return JsonResponse({"message": message})
