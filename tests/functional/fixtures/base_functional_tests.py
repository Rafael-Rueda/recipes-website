from time import sleep

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase

from apps.recipes import models
from apps.recipes.tests.fixtures.recipes_base_tests import RecipeMixin
from utils.browser import make_browser


class TestBase(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = make_browser()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, time=3):
        sleep(time)