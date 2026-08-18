from experiments.ch10_security_mechanisms.models import (
    AccessDecision,
    Protocol,
    Role,
    SecurityGroup,
    SecurityRule,
    User,
)

from experiments.ch10_security_mechanisms.iam import (
    IAMService,
)

from experiments.ch10_security_mechanisms.mfa import (
    MFAService,
)

from experiments.ch10_security_mechanisms.sso import (
    SSOService,
)

from experiments.ch10_security_mechanisms.security_group import (
    SecurityGroupEngine,
)

from experiments.ch10_security_mechanisms.encryption import (
    SymmetricEncryption,
)

from experiments.ch10_security_mechanisms.hashing import (
    HashingService,
)

from experiments.ch10_security_mechanisms.digital_signature import (
    DigitalSignatureService,
)


def demo_encryption():

    print("\n=== Encryption ===")

    encryption = SymmetricEncryption()

    encrypted = encryption.encrypt(
        "database-password"
    )

    print(
        "Encrypted:",
        encrypted,
    )

    print(
        "Decrypted:",
        encryption.decrypt(
            encrypted
        ),
    )


def demo_hashing():

    print("\n=== Hashing ===")

    hashing = HashingService()

    result = hashing.hash(
        "password"
    )

    print(result)

    print(
        "Valid:",
        hashing.verify(
            "password",
            result.digest,
        ),
    )


def demo_signature():

    print("\n=== Digital Signature ===")

    service = (
        DigitalSignatureService()
    )

    signature = service.sign(
        "deploy server"
    )

    print(
        "Valid:",
        service.verify(
            "deploy server",
            signature,
        ),
    )

    print(
        "Tampered:",
        service.verify(
            "delete server",
            signature,
        ),
    )


def demo_iam_mfa_sso():

    print(
        "\n=== IAM + MFA + SSO ==="
    )

    iam = IAMService()

    iam.add_user(
        User(
            user_id="user-001",
            username="alice",
            tenant_id="tenant-a",
        )
    )

    iam.add_role(
        Role(
            name="developer",
            permissions={
                "server:read",
                "server:start",
            },
        )
    )

    iam.assign_role(
        "user-001",
        "developer",
    )

    print(
        "Read:",
        iam.authorize(
            "user-001",
            "server:read",
        ),
    )

    print(
        "Delete:",
        iam.authorize(
            "user-001",
            "server:delete",
        ),
    )

    mfa = MFAService()

    code = mfa.generate_code(
        "user-001"
    )

    print(
        "MFA:",
        mfa.verify(
            "user-001",
            code,
        ),
    )

    sso = SSOService()

    token = sso.create_session(
        "user-001"
    )

    print(
        "SSO user:",
        sso.authenticate(token),
    )


def demo_security_group():

    print(
        "\n=== Security Group ==="
    )

    group = SecurityGroup(
        group_id="sg-api",
        rules=[
            SecurityRule(
                protocol=Protocol.TCP,
                port=443,
                source="0.0.0.0/0",
                action=AccessDecision.ALLOW,
            ),
            SecurityRule(
                protocol=Protocol.TCP,
                port=22,
                source="10.0.0.0/24",
                action=AccessDecision.ALLOW,
            ),
        ],
    )

    engine = SecurityGroupEngine(
        group
    )

    print(
        "HTTPS:",
        engine.evaluate(
            Protocol.TCP,
            443,
            "0.0.0.0/0",
        ),
    )

    print(
        "SSH from Internet:",
        engine.evaluate(
            Protocol.TCP,
            22,
            "0.0.0.0/0",
        ),
    )


def main():

    demo_encryption()

    demo_hashing()

    demo_signature()

    demo_iam_mfa_sso()

    demo_security_group()


if __name__ == "__main__":
    main()