import sys

import logging
from pages.pom import InternetStorePOM

logger = logging.getLogger("facade")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


class InternetStoreFacade:

    def __init__(self, page, screenshot_folder="screenshots", test_name="facade_test"):
        self.pom = InternetStorePOM(page)
        self.screenshot_folder = screenshot_folder
        self.test_name = test_name

    def login(self, username, password):
        self.pom.fill_username(username)
        self.pom.fill_password(password)
        self.pom.click_login_button()
        self.pom.take_screenshot(f"{self.screenshot_folder}\\{self.test_name}\\login.png")

    def add_to_shopping_cart(self, product_name):
        self.pom.click_add_button_for_product_name(product_name)
        self.pom.take_screenshot(f"{self.screenshot_folder}\\{self.test_name}\\{product_name}\\added_to_cart.png")
        self.pom.click_cart()
        self.pom.take_screenshot(f"{self.screenshot_folder}\\{self.test_name}\\{product_name}\\cart.png")
        return self.pom.get_cart_items()

    def add_and_remove_from_cart(self):
        self.pom.click_first_add_button()
        self.pom.click_remove_button()

    def add_first_item_to_cart(self):
        self.pom.click_first_add_button()

    def remove_first_item_to_cart(self):
        self.pom.click_remove_button()

    def click_twitter_button(self):
        self.pom.click_twitter_button()


    def click_social_link_button(self, socialLink):
        match socialLink:
            case "twitter":
                self.pom.click_twitter_button()
            case "facebook":
                self.pom.click_facebook_button()
            case "linkedin":
                self.pom.click_linkedin_button()
            case _:
                raise ValueError(f"Unknown social link: {value}")

    def get_cart_count(self):
        return self.pom.get_cart_count()

    def apply_sorting(self, sort_type):
        return self.pom.apply_sorting(sort_type)

    def click_cart(self):
         return self.pom.click_cart()

    def click_checkout(self):
        return self.pom.click_checkout_button()

    def fill_personal_info(self, first_name, last_name, postal_code):
        return self.pom.fill_personal_info(first_name, last_name, postal_code)

    def click_finish(self):
        return self.pom.click_finish_button()

    def has_fill_personal_info_error_badge(self):
        return self.pom.has_fill_personal_info_error_badge()

    def take_screenshot(self, path):
        self.pom.take_screenshot(path)