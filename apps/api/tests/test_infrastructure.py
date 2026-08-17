from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_token(username: str) -> str:

    response = client.post(
        f"/security/token?username={username}"
    )

    assert response.status_code == 200

    return response.json()[
        "access_token"
    ]


def test_tenant_can_create_server():

    token = get_token("alice")

    response = client.post(
        "/infrastructure/servers",
        params={
            "server_id": "alice-server-01",
            "cpu": 2,
            "memory_mb": 2048,
            "image": "ubuntu:24.04",
        },
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["tenant_id"]
        == "tenant-a"
    )

    assert (
        data["cpu"]
        == 2
    )


def test_unauthenticated_cannot_create_server():

    response = client.post(
        "/infrastructure/servers",
        params={
            "server_id": "unauthorized-server",
            "cpu": 2,
            "memory_mb": 2048,
            "image": "ubuntu:24.04",
        },
    )

    assert response.status_code == 401


def test_tenant_can_create_storage():

    token = get_token("alice")

    response = client.post(
        "/infrastructure/storage",
        params={
            "volume_id": "alice-volume-01",
            "size_gb": 20,
        },
        headers={
            "Authorization": (
                f"Bearer {token}"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["tenant_id"]
        == "tenant-a"
    )