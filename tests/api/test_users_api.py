import pytest

from conftest import new_email, register_user, strong_password

pytestmark = pytest.mark.api


@pytest.mark.parametrize(
    "path, expected_status",
    [("/users/me", 401), ("/products/does-not-exist", 404)],
    ids=["protected-profile", "missing-product"],
)
def test_user_or_product_missing_resource_returns_expected_4xx(api, path, expected_status):
    """Goal: verify documented client error responses.
    Precondition: no authentication header is supplied.
    Expected: protected and missing resources return their exact 4xx status."""
    response = api.get(path)
    assert response.status == expected_status, response.text()


def test_register_empty_body_reports_required_fields(api):
    """Goal: verify registration validation.
    Precondition: registration receives an empty JSON object.
    Expected: HTTP 422 includes email and password field errors."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    errors = response.json().get("errors", response.json())
    assert "email" in errors, response.text()
    assert "password" in errors, response.text()


def test_authenticated_profile_returns_the_created_user(api, auth_headers, test_user):
    """Goal: verify bearer-token authentication.
    Precondition: the session fixture created a unique test user and token.
    Expected: the profile response is 200 and contains that user's email."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"], response.text()


def test_register_new_user_response_does_not_expose_password(api):
    """Goal: verify registration does not leak secrets.
    Precondition: a unique email and generated strong password are used.
    Expected: registration returns 201 without a password field."""
    response = register_user(api, new_email(), strong_password())
    assert response.status == 201, response.text()
    assert "password" not in response.json(), response.text()
