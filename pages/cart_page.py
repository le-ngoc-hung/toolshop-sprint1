import re

from pages.base_page import BasePage


def money(text: str) -> float:
    """'$28.30' -> 28.3"""
    return float(text.replace("$", "").replace(",", "").strip())


class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)
        self.product_titles = page.get_by_test_id("product-title")
        self.quantities = page.get_by_test_id("product-quantity")
        self.line_prices = page.get_by_test_id("line-price")
        self.total = page.get_by_test_id("cart-total")
        self.continue_shopping = page.get_by_test_id("continue-shopping")

    def line_totals(self) -> list[float]:
        return [money(t) for t in self.line_prices.all_inner_texts()]

    def product_title(self, name: str):
        return self.product_titles.filter(has_text=re.compile(rf"^\s*{re.escape(name)}\s*$")).first

    def line_total(self) -> float:
        return money(self.line_prices.first.inner_text())

    def quantity_value(self) -> int:
        quantity = self.quantities.first
        return int(quantity.input_value() if quantity.input_value() else quantity.inner_text())

    def total_value(self) -> float:
        return money(self.total.inner_text())
