from dataclasses import dataclass


@dataclass
class SoftwarePackage:
    name: str
    installed_version: str
    latest_version: str


class SoftwareUpdateUtility:

    def check(
        self,
        package: SoftwarePackage,
    ) -> bool:

        return (
            package.installed_version
            == package.latest_version
        )

    def update(
        self,
        package: SoftwarePackage,
    ) -> None:

        package.installed_version = (
            package.latest_version
        )