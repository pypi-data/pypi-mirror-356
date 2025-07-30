import json
from dataclasses import dataclass
from datetime import datetime

import jwt
import requests
from google.cloud import secretmanager

from ssb_pubmd.request_handler import Response

TYPE = "JWT"
ALGORITHM = "RS256"


@dataclass
class SecretData:
    """Data class to hold private key and connected data."""

    private_key: str
    kid: str
    principal_key: str


class JWTRequestHandler:
    """This class is used to send requests with a JSON Web Token (JWT) in the header."""

    def __init__(self, gc_secret_resource_name: str) -> None:
        """Initializes a JWT request handler object."""
        self._gc_secret_resource_name: str = gc_secret_resource_name

    def _private_key_from_secret_manager(self) -> SecretData:
        """Fetches the private key from Google Cloud Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        print(f"Fetching secret from {self._gc_secret_resource_name}")
        response = client.access_secret_version(name=self._gc_secret_resource_name)
        raw_data = response.payload.data.decode("UTF-8")
        data = json.loads(raw_data)
        try:
            secret_data = SecretData(
                private_key=data["privateKey"],
                kid=data["kid"],
                principal_key=data["principalKey"],
            )
        except KeyError as e:
            raise ValueError(
                "The secret must be a JSON object with keys 'privateKey', 'kid' and 'principalKey'."
            ) from e
        return secret_data

    def _generate_token(self) -> str:
        secret_data = self._private_key_from_secret_manager()

        header = {
            "kid": secret_data.kid,
            "typ": TYPE,
            "alg": ALGORITHM,
        }

        iat = int(datetime.now().timestamp())
        exp = iat + 30
        payload = {
            "sub": secret_data.principal_key,
            "iat": iat,
            "exp": exp,
        }

        token = jwt.encode(
            payload, secret_data.private_key, algorithm=ALGORITHM, headers=header
        )
        return token

    def send_request(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
    ) -> Response:
        """Sends the request to the specified url with bearer token in header."""
        token = self._generate_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            url,
            headers=headers,
            json=data,
        )

        try:
            body = response.json()
            body = dict(body)
        except Exception:
            body = {}

        return Response(
            status_code=response.status_code,
            body=body,
        )
