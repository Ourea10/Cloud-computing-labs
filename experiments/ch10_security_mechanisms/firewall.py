from experiments.ch10_security_mechanisms.models import (
    AccessDecision,
    FirewallRule,
    Protocol,
)


class Firewall:

    def __init__(self):

        self.rules: list[
            FirewallRule
        ] = []

    def add_rule(
        self,
        rule: FirewallRule,
    ) -> None:

        self.rules.append(rule)

    def evaluate(
        self,
        protocol: Protocol,
        port: int,
        source: str,
        destination: str,
    ) -> AccessDecision:

        for rule in self.rules:

            if (
                rule.protocol == protocol
                and rule.port == port
                and rule.source == source
                and rule.destination
                == destination
            ):

                return rule.action

        return AccessDecision.DENY