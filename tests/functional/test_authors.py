import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.functional.fixtures.base_functional_tests import TestBase


@pytest.mark.functional
class RegisterTest(TestBase):
    def test_if_a_user_can_be_registred(self):
        self.browser.get(self.live_server_url + '/register')

        form = self.browser.find_element(By.XPATH, '//form[@action="/register/create/"]')

        username_input = form.find_element(By.XPATH, '//input[@name="username"]')
        email_input = form.find_element(By.XPATH, '//input[@name="email"]')
        first_name_input = form.find_element(By.XPATH, '//input[@name="first_name"]')
        last_name_input = form.find_element(By.XPATH, '//input[@name="last_name"]')
        password_input = form.find_element(By.XPATH, '//input[@name="password"]')
        password2_input = form.find_element(By.XPATH, '//input[@name="password2"]')
        submit_button = form.find_element(By.XPATH, '//button')

        # User type something on the fields and submit the form

        username_input.send_keys('test_user')
        email_input.send_keys('test@test.com')
        first_name_input.send_keys('test')
        last_name_input.send_keys('test')
        password_input.send_keys('test1234')
        password2_input.send_keys('test1234')

        submit_button.click()

        self.assertEqual(User.objects.first().username, 'test_user')

@pytest.mark.functional
class LoginTest(TestBase):
    def test_if_a_user_can_be_logged_in(self):

        self.make_recipe()

        self.browser.get(self.live_server_url + '/login')
        
        form = self.browser.find_element(By.XPATH, '//form[@action="/login/"]')

        username_input = form.find_element(By.XPATH, '//input[@name="username"]')
        password_input = form.find_element(By.XPATH, '//input[@name="password"]')
        submit_button = form.find_element(By.XPATH, '//button')


        username_input.send_keys('User')
        password_input.send_keys('123456')

        submit_button.click()

        self.assertIn('User logged in with success.', self.browser.find_element(By.TAG_NAME, 'body').text)
        