from experiments.ch01_introduction.resource import ComputeResource

from .case_model import CloudCase, ResourceRequirement
from .cloud_provider import CloudProvider


def create_provider() -> CloudProvider:
    provider = CloudProvider("test-provider")

    for number in range(5):
        provider.add_resource(
            ComputeResource(
                resource_id=f"server-{number}",
                cpu=8,
                memory=16384,
            )
        )

    return provider


def test_case_can_be_provisioned():
    provider = create_provider()

    case = CloudCase(
        name="ATN",
        resource_requirements=ResourceRequirement(
            cpu=4,
            memory=8192,
        ),
        desired_instances=2,
        characteristics=[],
    )

    resources = provider.provision_for_case(case)

    assert len(resources) == 2
    assert all(
        resource.allocated
        for resource in resources
    )


def test_resources_are_released():
    provider = create_provider()

    case = CloudCase(
        name="ATN",
        resource_requirements=ResourceRequirement(
            cpu=4,
            memory=8192,
        ),
        desired_instances=2,
        characteristics=[],
    )

    resources = provider.provision_for_case(case)

    provider.release_resources(resources)

    assert all(
        not resource.allocated
        for resource in resources
    )
