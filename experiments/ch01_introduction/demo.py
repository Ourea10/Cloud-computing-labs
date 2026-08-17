from resource import ComputeResource
from resource_pool import ResourcePool


def main():
    pool = ResourcePool()

    pool.add(
        ComputeResource(
            resource_id="server-01",
            cpu=4,
            memory=8192,
        )
    )

    pool.add(
        ComputeResource(
            resource_id="server-02",
            cpu=8,
            memory=16384,
        )
    )

    print("=== Initial Resource Pool ===")

    for item in pool.resources:
        print(
            item.resource_id,
            item.cpu,
            item.memory,
            item.allocated,
        )

    print("\n=== Consumer requests 2 CPU / 4GB ===")

    resource = pool.allocate(
        cpu=2,
        memory=4096,
    )

    print(
        f"Allocated: {resource.resource_id}"
    )

    print("\n=== Resource Pool After Allocation ===")

    for item in pool.resources:
        print(
            item.resource_id,
            item.cpu,
            item.memory,
            item.allocated,
        )

    print("\n=== Consumer releases resource ===")

    pool.release(resource.resource_id)

    print(
        f"Released: {resource.resource_id}"
    )


if __name__ == "__main__":
    main()
