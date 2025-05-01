import pytest
from utils.browser_factory import ChromiumBrowser, FirefoxBrowser, BrowserCreator
from playwright.sync_api import sync_playwright

@pytest.fixture(params=["chromium", "firefox"])
def browser(request) -> BrowserCreator:
    with sync_playwright() as p:
        if request.param == "chromium":
            yield ChromiumBrowser(p)
        elif request.param == "firefox":
            yield FirefoxBrowser(p)