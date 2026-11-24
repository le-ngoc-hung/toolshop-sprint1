import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.cart_page import CartPage
from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart.feature")


@given("I am on the home page", target_fixture="home")
def home(page):
    home_page = HomePage(page).open()
    expect(home_page.product_names.first).to_be_visible()
    return home_page


@when(parsers.parse('I open the product "{product}"'), target_fixture="product_page")
def open_product(home, product):
    product_page = home.open_product(product)
    expect(product_page.name).to_have_text(product)
    return product_page


@when(parsers.parse("I add it to the cart with quantity {quantity:d}"), target_fixture="unit_price")
def add_to_cart(product_page, quantity):
    unit_price = product_page.price()
    product_page.add_to_cart(quantity=quantity)
    return unit_price


@when("I open the cart", target_fixture="cart")
def open_cart(product_page):
    return product_page.go_to_cart()


@then(parsers.parse('the cart contains product "{product}"'))
def cart_contains_product(cart: CartPage, product):
    expect(cart.product_title(product)).to_have_text(product)


@then("the line price equals the unit price times quantity")
def line_price_equals_unit_price_times_quantity(cart, unit_price):
    quantity = int(cart.quantities.first.inner_text())
    assert cart.line_total() == pytest.approx(unit_price * quantity)


@then("the cart total equals the sum of the line prices")
def cart_total_equals_sum_of_line_prices(cart):
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))
