import pytest

pytestmark = pytest.mark.api


@pytest.fixture
def new_cart(api):
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


def test_cart_add_product_quantity_two_is_persisted(api, new_cart):
    """Goal: verify cart creation and item persistence.
    Precondition: a fresh cart is created by the fixture.
    Expected: POST then GET shows one selected product with quantity two."""
    products = api.get("/products", params={"page": 1})
    assert products.status == 200, products.text()
    product_id = products.json()["data"][0]["id"]

    add_item = api.post(
        f"/carts/{new_cart}",
        data={"product_id": product_id, "quantity": 2},
    )
    assert add_item.status in (200, 201), add_item.text()

    cart = api.get(f"/carts/{new_cart}")
    assert cart.status == 200, cart.text()
    items = cart.json().get("cart_items", cart.json().get("items", cart.json().get("products", [])))
    assert len(items) == 1, cart.text()
    assert items[0].get("product_id", items[0].get("id")) == product_id, cart.text()
    assert items[0]["quantity"] == 2, cart.text()
