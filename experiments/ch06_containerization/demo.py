from .container_model import (
    Container,
    ContainerHost,
)

from .image_model import (
    ContainerImage,
    ImageLayer,
)


def run_image_demo():
    print("=== Container Image ===")

    image = ContainerImage(
        name="cloud-lab-api",
        tag="1.0",
        layers=[
            ImageLayer(
                layer_id="python-runtime",
                size_mb=120,
            ),
            ImageLayer(
                layer_id="application",
                size_mb=20,
            ),
        ],
    )

    print(
        f"Image: {image.reference}"
    )

    print(
        f"Size: {image.size_mb} MB"
    )


def run_container_demo():
    print("\n=== Container ===")

    host = ContainerHost(
        host_id="docker-host-01",
        cpu=4,
        memory_mb=4096,
    )

    api = Container(
        container_id="api-01",
        image="cloud-lab-api:1.0",
        cpu_limit=1,
        memory_limit_mb=512,
    )

    worker = Container(
        container_id="worker-01",
        image="cloud-lab-worker:1.0",
        cpu_limit=1,
        memory_limit_mb=512,
    )

    host.run_container(api)
    host.run_container(worker)

    for container in host.containers:
        print(
            container.container_id,
            container.image,
            container.running,
        )


def main():
    run_image_demo()
    run_container_demo()


if __name__ == "__main__":
    main()
