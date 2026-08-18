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

from experiments.ch10_security_mechanisms.sso import (
    SSOService,
)

from experiments.ch10_security_mechanisms.vpn import (
    VPNService,
)


class CloudSecurityService:

    def __init__(self):

        self.encryption = (
            SymmetricEncryption()
        )

        self.hashing = (
            HashingService()
        )

        self.digital_signature = (
            DigitalSignatureService()
        )

        self.iam = IAMService()

        self.mfa = MFAService()

        self.sso = SSOService()

        self.vpn = VPNService(
            gateway="10.0.0.1"
        )