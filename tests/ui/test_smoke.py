import re

import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_search_pliers(page):
    """Goal: verify product search.
    Precondition: the Toolshop home page is available.
    Expected: every visible result contains 'pliers'."""
    home = HomePage(page).open().search("pliers")
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "search returned no products"
    assert all("pliers" in name.lower() for name in names), names


@pytest.mark.smoke
def test_add_claw_hammer_quantity_three(page):
    """Goal: verify adding a chosen product quantity.
    Precondition: Claw Hammer is available.
    Expected: the cart badge shows 3 after adding the product."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_have_text("Claw Hammer")
    product.add_to_cart(quantity=3)
    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
def test_invalid_login_is_rejected(page):
    """Goal: verify invalid login handling.
    Precondition: the test email does not belong to a real account.
    Expected: an error is shown and the login route remains open."""
    login = LoginPage(page).open().login("nobody-here@example.invalid", "Wrong-Password-123")
    expect(login.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
def test_empty_contact_form_shows_required_errors(page):
    """Goal: verify required validation on the contact form.
    Precondition: the contact page is available.
    Expected: subject and message required errors are visible."""
    contact = ContactPage(page).open()
    contact.submit()
    expect(contact.errors.filter(has_text="Subject is required")).to_be_visible()
    expect(contact.errors.filter(has_text="Message is required")).to_be_visible()
