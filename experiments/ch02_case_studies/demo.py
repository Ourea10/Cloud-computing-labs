from experiments.ch01_introduction.resource import ComputeResource

from .case_loader import load_cases
from .cloud_provider import CloudProvider


def create_provider() -> CloudProvider:
    provider = CloudProvider(
        name="CloudLab Provider"
    )

    for number in range(1, 11):
        provider.add_resource(
            ComputeResource(
                resource_id=f"server-{number:02d}",
                cpu=8,
                memory=16384,
            )
        )

    return provider


def main():
    provider = create_provider()
    cases = load_cases()

    for case in cases.values():
        print(f"\n=== {case.name} ===")

        resources = provider.provision_for_case(case)

        print(
            f"Provisioned {len(resources)} resources:"
        )

        for resource in resources:
            print(
                f"  - {resource.resource_id}"
            )

        provider.release_resources(resources)

        print("Resources released.")


if __name__ == "__main__":
    main()
