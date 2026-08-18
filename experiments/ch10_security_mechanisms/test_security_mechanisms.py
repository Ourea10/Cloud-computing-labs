from experiments.ch10_security_mechanisms.encryption import (
    SymmetricEncryption,
)

from experiments.ch10_security_mechanisms.hashing import (
    HashingService,
)

from experiments.ch10_security_mechanisms.digital_signature import (
    DigitalSignatureService,
)

from experiments.ch10_security_mechanisms.iam import (
    IAMService,
)

from experiments.ch10_security_mechanisms.mfa import (
    MFAService,
)

from experiments.ch10_security_mechanisms.models import (
    AccessDecision,
    Protocol,
    Role,
    SecurityGroup,
    SecurityRule,
    User,
)

from experiments.ch10_security_mechanisms.security_group import (
    SecurityGroupEngine,
)


def test_encryption_round_trip():

    service = SymmetricEncryption()

    encrypted = service.encrypt(
        "hello"
    )

    assert (
        service.decrypt(encrypted)
        == "hello"
    )


def test_hashing():

    service = HashingService()

    result = service.hash(
        "password"
    )

    assert service.verify(
        "password",
        result.digest,
    )

    assert not service.verify(
        "wrong-password",
        result.digest,
    )


def test_digital_signature():

    service = (
        DigitalSignatureService()
    )

    signature = service.sign(
        "message"
    )

    assert service.verify(
        "message",
        signature,
    )

    assert not service.verify(
        "tampered",
        signature,
    )


def test_iam_authorization():

    iam = IAMService()

    iam.add_user(
        User(
            user_id="user-1",
            username="alice",
            tenant_id="tenant-a",
        )
    )

    iam.add_role(
        Role(
            name="developer",
            permissions={
                "server:read"
            },
        )
    )

    iam.assign_role(
        "user-1",
        "developer",
    )

    assert (
        iam.authorize(
            "user-1",
            "server:read",
        )
        == AccessDecision.ALLOW
    )

    assert (
        iam.authorize(
            "user-1",
            "server:delete",
        )
        == AccessDecision.DENY
    )


def test_mfa():

    service = MFAService()

    code = service.generate_code(
        "user-1"
    )

    assert service.verify(
        "user-1",
        code,
    )

    assert not service.verify(
        "user-1",
        code,
    )


def test_security_group():

    group = SecurityGroup(
        group_id="sg-1",
        rules=[
            SecurityRule(
                protocol=Protocol.TCP,
                port=443,
                source="0.0.0.0/0",
                action=AccessDecision.ALLOW,
            )
        ],
    )

    engine = SecurityGroupEngine(
        group
    )

    assert (
        engine.evaluate(
            Protocol.TCP,
            443,
            "0.0.0.0/0",
        )
        == AccessDecision.ALLOW
    )

    assert (
        engine.evaluate(
            Protocol.TCP,
            22,
            "0.0.0.0/0",
        )
        == AccessDecision.DENY
    )