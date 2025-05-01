import logging
from playwright.sync_api import sync_playwright, expect
import os
import sys
import pytest
from pages.pom import InternetStorePOM
from pages.facade import InternetStoreFacade
from dotenv import load_dotenv
import time

load_dotenv("config/.env")


logger = logging.getLogger("test")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

@pytest.mark.parametrize("social_media, expected_url", [
   ("twitter", "https://x.com/saucelabs"),
   ("facebook", "https://www.facebook.com/saucelabs"),
   ("linkedin", "https://www.linkedin.com/company/sauce-labs/"),
])
def test_expects_social_opened(social_media, expected_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(os.environ['SITE_URL'])

        int_store = InternetStoreFacade(page)
        int_store.login(os.environ['USER_NAME'], os.environ['PASSWORD'])

        with page.context.expect_page() as new_page_info:
            int_store.click_social_link_button(social_media)
        new_page = new_page_info.value

        time.sleep(2)
        new_page.screenshot(path="screenshots/test_"+ social_media + "_social_media.png")
        expect(new_page).to_have_url(expected_url)

def test_expects_checkout_badge_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(os.environ['SITE_URL'])

        int_store = InternetStoreFacade(page)
        int_store.login(os.environ['USER_NAME'], os.environ['PASSWORD'])
        int_store.add_first_item_to_cart()
        int_store.add_first_item_to_cart()
        int_store.remove_first_item_to_cart()

        items_count = int_store.get_cart_count()

        assert 1 == items_count, f"Products in the shopping cart must be 2, got {items_count}"

@pytest.mark.parametrize("sort_type, expected_first_item_name", [
   ("az", "Sauce Labs Backpack"),
   ("za", "Test.allTheThings() T-Shirt (Red)"),
   ("lohi", "Sauce Labs Onesie"),
   ("hilo", "Sauce Labs Fleece Jacket"),
])
def test_sorting_expects_correctly(sort_type, expected_first_item_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(os.environ['SITE_URL'])

        int_store = InternetStoreFacade(page)
        int_store.login(os.environ['USER_NAME'], os.environ['PASSWORD'])
        int_store.apply_sorting(sort_type)
        first_item_name = int_store.pom.get_first_item_name()

        assert expected_first_item_name == first_item_name, f"Products in the shopping cart must be 2, got {items_count}"


def test_create_order_expects_created():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(os.environ['SITE_URL'])

        int_store = InternetStoreFacade(page)
        int_store.login(os.environ['USER_NAME'], os.environ['PASSWORD'])
        int_store.add_first_item_to_cart()
        int_store.click_cart()
        page.wait_for_load_state('load')
        int_store.click_checkout()
        int_store.fill_personal_info("sanya", "polosmak", "14001")
        int_store.click_finish()

        assert "https://www.saucedemo.com/checkout-complete.html" == page.url, f"Current page is {page.url}, should https://www.saucedemo.com/checkout-complete.html"


def test_create_order_expects_fail_if_missing_user_name():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(os.environ['SITE_URL'])

        int_store = InternetStoreFacade(page)
        int_store.login(os.environ['USER_NAME'], os.environ['PASSWORD'])
        int_store.add_first_item_to_cart()
        int_store.click_cart()
        page.wait_for_load_state('load')
        int_store.click_checkout()
        int_store.fill_personal_info("", "polosmak", "14001")
        has_error_badge = int_store.has_fill_personal_info_error_badge()

        assert True == has_error_badge, f"Error badge should be present, but it is not"
