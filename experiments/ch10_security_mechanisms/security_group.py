from experiments.ch10_security_mechanisms.models import (
    AccessDecision,
    Protocol,
    SecurityGroup,
    SecurityRule,
)


class SecurityGroupEngine:

    def __init__(
        self,
        security_group: SecurityGroup,
    ):

        self.security_group = security_group

    def evaluate(
        self,
        protocol: Protocol,
        port: int,
        source: str,
    ) -> AccessDecision:

        for rule in self.security_group.rules:

            if (
                rule.protocol == protocol
                and rule.port == port
                and (
                    rule.source == source
                    or rule.source == "0.0.0.0/0"
                )
            ):

                return rule.action

        return AccessDecision.DENY