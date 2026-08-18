import secrets

from datetime import timedelta

from experiments.ch10_security_mechanisms.models import (
    Certificate,
    utc_now,
)


class CertificateAuthority:

    def __init__(
        self,
        name: str,
    ):

        self.name = name

        self.certificates: dict[
            str,
            Certificate,
        ] = {}

    def issue_certificate(
        self,
        subject: str,
        public_key: str,
        validity_days: int = 365,
    ) -> Certificate:

        certificate = Certificate(
            subject=subject,
            issuer=self.name,
            serial_number=secrets.token_hex(16),
            public_key=public_key,
            valid_from=utc_now(),
            valid_until=(
                utc_now()
                + timedelta(
                    days=validity_days
                )
            ),
        )

        self.certificates[
            certificate.serial_number
        ] = certificate

        return certificate

    def verify(
        self,
        certificate: Certificate,
    ) -> bool:

        if certificate.issuer != self.name:
            return False

        now = utc_now()

        return (
            certificate.valid_from
            <= now
            <= certificate.valid_until
        )