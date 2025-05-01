from abc import ABC, abstractmethod


class BrowserCreator(ABC):
    def __init__(self, p, is_headless = False):
        self.p = p
        self.is_headless = is_headless
    @abstractmethod
    def browser_factory(self):
        pass
    def new_page(self):
        browser = self.browser_factory()
        return browser.new_page()


class ChromiumBrowser(BrowserCreator):
    def browser_factory(self):
        return self.p.chromium.launch(headless=self.is_headless)

class FirefoxBrowser(BrowserCreator):
    def browser_factory(self):
        return self.p.firefox.launch(headless=self.is_headless)
