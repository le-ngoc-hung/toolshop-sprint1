import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.api

KEYWORDS = json.loads(
    (Path(__file__).parents[2] / "data" / "search_keywords.json").read_text(encoding="utf-8")
)


def test_products_first_page_has_valid_pagination_and_product_shape(api):
    """Goal: validate the products contract.
    Precondition: the Toolshop API is available.
    Expected: pagination keys and sane fields for every returned product."""
    response = api.get("/products", params={"page": 1})
    assert response.status == 200, response.text()
    body = response.json()
    for key in ("current_page", "data", "per_page", "total", "last_page"):
        assert key in body, f"missing key {key}: {response.text()}"
    assert 0 < len(body["data"]) <= body["per_page"], response.text()
    for product in body["data"]:
        assert isinstance(product["id"], (str, int)), response.text()
        assert isinstance(product["name"], str) and product["name"].strip(), response.text()
        assert isinstance(product["price"], (int, float)) and product["price"] > 0, response.text()


@pytest.mark.parametrize("case", KEYWORDS, ids=[case["keyword"] for case in KEYWORDS])
def test_product_search_keyword_returns_matching_products(api, case):
    """Goal: verify data-driven product search.
    Precondition: search keywords are loaded from the JSON data file.
    Expected: every returned product name contains the requested keyword."""
    response = api.get("/products/search", params={"q": case["keyword"]})
    assert response.status == 200, response.text()
    names = [product["name"] for product in response.json()["data"]]
    assert names, f"no results for {case['keyword']}: {response.text()}"
    assert all(case["must_contain"] in name.lower() for name in names), response.text()
