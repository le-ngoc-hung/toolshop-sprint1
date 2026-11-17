import re

import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_search_unknown_keyword_shows_empty_state(page):
    """Goal: verify an unknown search term.
    Precondition: the home page is loaded.
    Expected: the no-results message is shown and no product cards remain."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


def test_sort_products_by_price_ascending(page):
    """Goal: verify price sorting.
    Precondition: the home page has loaded its product list.
    Expected: visible prices are ordered from low to high."""
    home = HomePage(page).open().sort_by("price,asc")
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices == sorted(prices), prices


def test_filter_hammer_category_shows_matching_products(page):
    """Goal: verify category filtering.
    Precondition: the product list is available and the Hammer category exists.
    Expected: every visible product name contains hammer."""
    home = HomePage(page).open().filter_by_category("Hammer")
    expect(home.product_names.first).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "category filter returned no products"
    assert all("hammer" in name.lower() for name in names), names


def test_product_detail_shows_name_and_positive_price(page):
    """Goal: verify product detail data.
    Precondition: Claw Hammer is listed on the home page.
    Expected: detail name is exact and price is positive."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_have_text("Claw Hammer")
    assert product.price() > 0


def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: verify cart arithmetic.
    Precondition: a fresh browser context and Combination Pliers are available.
    Expected: line price equals unit price multiplied by quantity two."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit_price = product.price()
    product.add_to_cart(quantity=2)
    cart = product.go_to_cart()
    expect(cart.product_titles.first).to_be_visible()
    assert cart.line_totals() == [pytest.approx(unit_price * 2)]


def test_cart_continue_shopping_returns_to_product_grid(page):
    """Goal: verify the cart navigation flow.
    Precondition: one Hammer has been added to a fresh cart.
    Expected: Continue Shopping returns to a visible product grid."""
    cart = HomePage(page).open().open_product("Hammer").add_to_cart().go_to_cart()
    cart.continue_shopping.click()
    expect(HomePage(page).product_names.first).to_be_visible()


def test_empty_login_form_shows_required_errors(page):
    """Goal: verify empty login validation.
    Precondition: the login page is open with no fields filled.
    Expected: required errors are visible for email and password."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")


def test_my_account_shows_user_menu_after_storage_login(logged_in_page):
    """Goal: verify reuse of authenticated storage state.
    Precondition: logged_in_page creates an independent context from auth_state.
    Expected: My account and the QA Bot menu are visible."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
