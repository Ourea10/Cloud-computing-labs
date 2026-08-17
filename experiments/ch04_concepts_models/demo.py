from experiments.ch01_introduction.resource import ComputeResource

from .cloud_environment import CloudEnvironment
from .tenant import Tenant


def main() -> None:
    environment = CloudEnvironment()

    environment.register_tenant(
        Tenant(tenant_id="tenant-a", name="Company A")
    )
    environment.register_tenant(
        Tenant(tenant_id="tenant-b", name="Company B")
    )

    for number in range(1, 4):
        environment.add_resource(
            ComputeResource(
                resource_id=f"server-{number:02d}",
                cpu=8,
                memory=16384,
            )
        )

    resource = environment.allocate(
        tenant_id="tenant-a",
        cpu=4,
        memory=4096,
    )

    print("=== Cloud Environment ===")
    print(f"Tenant A allocated: {resource.resource_id}")
    print(
        "Tenant A resources:",
        [
            item.resource_id
            for item in environment.resources_for_tenant("tenant-a")
        ],
    )

    environment.release("tenant-a", resource.resource_id)
    print(f"Released: {resource.resource_id}")


if __name__ == "__main__":
    main()
