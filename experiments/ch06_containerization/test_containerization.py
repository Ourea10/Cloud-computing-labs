import pytest

from .container_model import (
    Container,
    ContainerHost,
)

from .image_model import (
    ContainerImage,
    ImageLayer,
)


def test_container_starts():
    container = Container(
        container_id="container-01",
        image="api:1.0",
        cpu_limit=1,
        memory_limit_mb=512,
    )

    container.start()

    assert container.running is True


def test_container_host_tracks_resources():
    host = ContainerHost(
        host_id="host-01",
        cpu=4,
        memory_mb=4096,
    )

    container = Container(
        container_id="container-01",
        image="api:1.0",
        cpu_limit=1,
        memory_limit_mb=512,
    )

    host.run_container(container)

    assert host.used_cpu == 1
    assert host.used_memory == 512


def test_host_rejects_overallocation():
    host = ContainerHost(
        host_id="host-01",
        cpu=1,
        memory_mb=512,
    )

    first = Container(
        container_id="container-01",
        image="api:1.0",
        cpu_limit=1,
        memory_limit_mb=512,
    )

    second = Container(
        container_id="container-02",
        image="api:1.0",
        cpu_limit=1,
        memory_limit_mb=512,
    )

    host.run_container(first)

    with pytest.raises(RuntimeError):
        host.run_container(second)


def test_image_size():
    image = ContainerImage(
        name="api",
        tag="1.0",
        layers=[
            ImageLayer("base", 100),
            ImageLayer("app", 20),
        ],
    )

    assert image.size_mb == 120
