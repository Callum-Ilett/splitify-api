"""
Utility functions for the Auth0 authorization package.
"""

from __future__ import annotations

import json

import jwt
import requests
from django.contrib.auth import authenticate


class PublicKeyNotFoundError(Exception):
    """Raised when JWT public key is not found."""


def jwt_get_username_from_payload_handler(payload: dict[str, str]) -> str:
    """
    Get the username from the payload.
    """
    username = payload.get("sub", "").replace("|", ".")

    authenticate(remote_user=username)
    return username


# pylint: disable=broad-except,missing-docstring,invalid-name
def jwt_decode_token(token: str) -> dict[str, str]:
    """
    Decode the token.
    """
    header = jwt.get_unverified_header(token)
    jwks = requests.get(
        "https://{}/.well-known/jwks.json".format("dev-282pztsm.eu.auth0.com"),
        timeout=5,
    ).json()

    public_key: str | None = None

    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))  # type: ignore  # noqa: PGH003

    if public_key is None:
        public_key_message = "Public key not found."
        raise PublicKeyNotFoundError(public_key_message)

    issuer = "https://{}/".format("dev-282pztsm.eu.auth0.com")
    return jwt.decode(
        token,
        public_key,  # type: ignore  # noqa: PGH003
        audience="https://splitify.com/api",
        issuer=issuer,
        algorithms=["RS256"],
    )
