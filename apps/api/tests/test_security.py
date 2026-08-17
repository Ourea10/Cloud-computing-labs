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


def test_authenticated_user_can_access_own_tenant():
    token = get_token("alice")

    response = client.get(
        "/security/resources/resource-a",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200


def test_cross_tenant_access_is_denied():
    token = get_token("alice")

    response = client.get(
        "/security/resources/resource-b",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_missing_authentication_is_denied():
    response = client.get(
        "/security/resources/resource-a"
    )

    assert response.status_code == 401


def test_admin_can_access_other_tenant():
    token = get_token("admin")

    response = client.get(
        "/security/resources/resource-b",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200