from typing import Any, Callable, Mapping, TypedDict
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import inject
import josepy
from cryptography import x509
from cryptography.x509.oid import NameOID
import pytest
from acmev2.handlers import handle, NewAccountRequestHandler

from acmev2.models import (
    OrderResource,
    OrderStatus,
    AuthorizationStatus,
    ChallengeStatus,
    NewAccountRequestSchema,
    AuthorizationResource,
)
from acmev2.handlers import ACMEModelResponse
from acmev2.services import (
    IDirectoryService,
    IChallengeService,
    ACMEEndpoint,
    IAuthorizationService,
)


def resp_has_error(resp: ACMEModelResponse, err: str, detail: str = None) -> bool:
    err_msg = resp.msg.model_dump()
    valid = err_msg.get("type") == err
    if detail:
        valid = valid and err_msg.get("detail") == detail

    return valid


def gen_private_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def gen_jwk_rsa(private_key: rsa.RSAPrivateKey):
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return josepy.JWKRSA.load(pem_private_key)


def gen_encoded_csr(*args, **kwargs) -> bytes:
    return josepy.encode_b64jose(
        gen_csr(*args, **kwargs).public_bytes(serialization.Encoding.DER)
    )


def gen_csr(
    key: rsa.RSAPrivateKey,
    cn: str = None,
    sans: list[str] = ["test.localhost", "test2.localhost"],
    order: OrderResource = None,
):
    if order:
        cn = order.identifiers[0].value
        sans = [order.identifiers[0].value] + [i.value for i in order.identifiers]

    builder = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, cn),
            ]
        )
    )

    if sans:
        builder = builder.add_extension(
            x509.SubjectAlternativeName(
                [
                    # Describe what sites we want this certificate for.
                    x509.DNSName(n)
                    for n in sans
                ]
            ),
            critical=False,
            # Sign the CSR with our private key.
        )
    csr = builder.sign(key, hashes.SHA256())

    return csr


def make_order_ready(order: OrderResource):
    order.status = OrderStatus.ready
    for authz in order.authorizations:
        authz.status = AuthorizationStatus.valid
        authz.challenges[0].status = ChallengeStatus.valid


def chall_by_url(url: str):
    directory_service = inject.instance(IDirectoryService)
    chall_service = inject.instance(IChallengeService)
    return chall_service.get(
        directory_service.identifier_from_url(ACMEEndpoint.challenge, url)
    )


def authz_by_url(url: str):
    directory_service = inject.instance(IDirectoryService)
    authz_service = inject.instance(IAuthorizationService)
    return authz_service.get(
        directory_service.identifier_from_url(ACMEEndpoint.authz, url)
    )


def validate_authz(authz: AuthorizationResource):
    authz.challenges[0].status = ChallengeStatus.valid
    authz.status = AuthorizationStatus.valid
