import os
import logging
import sys


logger = logging.getLogger("pom")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


class InternetStorePOM:

    def __init__(self, page):
        self.page = page

        self.button_login = page.query_selector('#login-button')
        self.username_input = page.locator('input[name="user-name"]')
        self.password_input = page.locator('input[name="password"]')
        self.link_cart = page.locator('a.shopping_cart_link')

        self.button_add_to_cart = page.locator("button.btn.btn_primary.btn_small.btn_inventory")
        self.button_remove_from_cart = page.locator("button#remove-sauce-labs-backpack")
        self.shopping_cart_badge = page.locator("span.shopping_cart_badge")
        self.sort_select = page.locator("select.product_sort_container")
        self.inventory_item_names = page.locator("div.inventory_item_name")

        self.button_checkout = page.locator("button#checkout")
        self.item_in_cart_badge = page.locator("span.shopping_cart_badge")

        self.finish_order_creating_button = page.locator("button#finish")

    def fill_username(self, input):
        self.username_input.fill(input)
        logger.info("Fill username")

    def fill_password(self, password):
        self.password_input.fill(password)
        logger.info("Fill password")

    def click_login_button(self):
        self.button_login.click()
        logger.info("Click login button")

    def click_first_add_button(self):
        self.button_add_to_cart.first.click()
        logger.info("Click add button")

    def get_cart_count(self):
        return int(self.shopping_cart_badge.text_content())

    def get_first_item_name(self):
        return self.inventory_item_names.first.text_content()

    def get_shopping_cart_badge_count(self):
        return self.shopping_cart_badge.count()

    def click_remove_button(self):
        self.button_remove_from_cart.first.click()
        logger.info("Click remove button")

    def click_cart(self):
        self.link_cart.click()
        logger.info("Successfully clicked cart")

    def click_add_button_for_product_name(self, product_name):
        child = self.inventory_item_names.filter(has_text=product_name)
        button = self.page.locator("div.inventory_item_description")\
            .filter(has=child)\
            .locator('button.btn.btn_primary.btn_small.btn_inventory')
        logger.info(button)
        button.click()
        logger.info("Click add product button")

    def get_cart_items(self):
        count = self.inventory_item_names.count()
        return [self.inventory_item_names.nth(i).text_content() for i in range(count)]

    def take_screenshot(self, path):
        self.page.wait_for_load_state('load')
        self.page.screenshot(path=path)


    def click_twitter_button(self):
        self.page.locator("a[data-test=social-twitter]").click()
        self.page.wait_for_load_state('load')
        logger.info("Click Twitter page")

    def click_linkedin_button(self):
        self.page.locator("a[data-test=social-linkedin]").click()
        self.page.wait_for_load_state('load')
        logger.info("Click Twitter page")

    def click_facebook_button(self):
        self.page.locator("a[data-test=social-facebook]").click()
        self.page.wait_for_load_state('load')
        logger.info("Click Twitter page")

    def get_item_in_cart_count(self):
        return self.item_in_cart_badge.count()

    def apply_sorting(self, sort_type):
        self.sort_select.select_option(sort_type)

    def fill_personal_info(self, first_name, last_name, postal_code):
        self.page.locator("input#first-name").fill(first_name)
        self.page.locator("input#last-name").fill(last_name)
        self.page.locator("input#postal-code").fill(postal_code)
        self.page.locator("input#continue").click()

    def click_checkout_button(self):
        self.button_checkout.click()
        logger.info("Click checkout button")

    def click_finish_button(self):
        self.finish_order_creating_button.click()
        logger.info("Click finish button")

    def has_fill_personal_info_error_badge(self):
        self.page.locator("input#continue").click()
        error_badge = self.page.locator('[data-test="error-button"]')
        return error_badge.is_visible()
