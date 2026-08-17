from dataclasses import dataclass, field

from experiments.ch08_infrastructure.models import (
    NetworkProtocol,
    NetworkRule,
)


@dataclass
class LogicalNetworkPerimeter:

    name: str

    rules: list[NetworkRule] = field(
        default_factory=list
    )

    def add_rule(
        self,
        protocol: NetworkProtocol,
        port: int,
        source: str,
        action: str,
    ) -> None:

        self.rules.append(
            NetworkRule(
                protocol=protocol,
                port=port,
                source=source,
                action=action,
            )
        )

    def allows(
        self,
        protocol: NetworkProtocol,
        port: int,
        source: str,
    ) -> bool:

        for rule in self.rules:

            if (
                rule.protocol == protocol
                and rule.port == port
                and (
                    rule.source == source
                    or rule.source == "0.0.0.0/0"
                )
            ):
                return rule.action == "allow"

        return False