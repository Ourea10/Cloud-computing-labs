from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    resource_id: str
    severity: str
    description: str


class PenetrationTestingTool:

    def scan_configuration(
        self,
        resource_id: str,
        open_ports: set[int],
    ) -> list[Finding]:

        findings = []

        if 23 in open_ports:

            findings.append(
                Finding(
                    resource_id=resource_id,
                    severity="high",
                    description=(
                        "Telnet port 23 "
                        "is exposed"
                    ),
                )
            )

        if 21 in open_ports:

            findings.append(
                Finding(
                    resource_id=resource_id,
                    severity="medium",
                    description=(
                        "FTP port 21 "
                        "is exposed"
                    ),
                )
            )

        return findings