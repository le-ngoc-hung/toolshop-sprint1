import json
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage, PRODUCT_LIST

pytestmark = pytest.mark.ui

EMPTY_PAGE = {
    "current_page": 1,
    "data": [],
    "from": None,
    "last_page": 1,
    "per_page": 9,
    "to": None,
    "total": 0,
}


def test_home_blocks_images_but_keeps_products_visible(page):
    """Goal: verify image requests can be blocked safely.
    Precondition: the image route is registered before opening the home page.
    Expected: at least one image is aborted and product names remain visible."""
    blocked = []

    def block(route):
        blocked.append(route.request.url)
        route.abort()

    page.route(re.compile(r"\.(png|jpe?g|webp|avif|svg)(\?.*)?$", re.IGNORECASE), block)
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    assert blocked, "no image request was blocked"


def test_home_empty_products_shows_no_results(page):
    """Goal: verify the empty product state through network mocking.
    Precondition: only the product-list endpoint is fulfilled with an empty page.
    Expected: the no-results message is visible and no product card is rendered."""
    page.route(
        PRODUCT_LIST,
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(EMPTY_PAGE),
        ),
    )
    home = HomePage(page).open()
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)
