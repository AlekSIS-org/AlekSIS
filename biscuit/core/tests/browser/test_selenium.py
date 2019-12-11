import os

import pytest

from django.test import LiveServerTestCase

webdriver = pytest.importorskip('selenium.webdriver')


class SeleniumTests(LiveServerTestCase):
    __test__ = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium.set_window_size(1920, 1080)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def _screenshot(cls, filename):
        screenshot_path = os.environ.get('TEST_SCREENSHOT_PATH', None)
        if screenshot_path:
            return cls.selenium.save_screenshot(os.path.join(screenshot_path, filename))
        else:
            return False

    @pytest.mark.django_db
    def test_index(self):
        self.selenium.get(self.live_server_url + '/')
        assert 'BiscuIT' in self.selenium.title
        self._screenshot('index.png')


class SeleniumTestsChromium(SeleniumTests):
    __test__ = True

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-impl-side-painting")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-seccomp-filter-sandbox")
        options.add_argument("--disable-breakpad")
        options.add_argument("--disable-client-side-phishing-detection")
        options.add_argument("--disable-cast")
        options.add_argument("--disable-cast-streaming-hw-encoding")
        options.add_argument("--disable-cloud-import")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-session-crashed-bubble")

        cls.selenium = webdriver.Chrome(options=options)

        super().setUpClass()
