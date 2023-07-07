from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.functional.fixtures.base_functional_tests import TestBase


@pytest.mark.functional
class HomeTests(TestBase):

    @patch('apps.recipes.views.PER_PAGE', new=2)
    def test_if_home_page_loads(self):
        self.make_recipes(len=6)
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.CSS_SELECTOR, value='body')
        self.assertIn('Test', body.text)

    def test_if_search_input_works_correctly(self):
        recipes = self.make_recipes(len=6)
        expected_text = 'Test Recipe !'
        recipes[0].title = expected_text
        recipes[0].save()


        # Open the browser in the site URL
        self.browser.get(self.live_server_url)

        # User makes a search
        input_element = self.browser.find_element(By.CLASS_NAME, 'search-form-content-input')
        input_element.send_keys('Test Recipe !')
        input_element.send_keys(Keys.ENTER)
        
        self.assertIn(expected_text, self.browser.find_element(By.TAG_NAME, 'body').text)

    @patch('apps.recipes.views.PER_PAGE', new=2)
    def test_if_pagination_works_correctly(self):
        
        recipes = self.make_recipes(len=12)

        # Open the browser in the site URL
        self.browser.get(self.live_server_url)

        # User clicks on the paginator "page 2" button

        page2 = self.browser.find_element(By.XPATH, '//a[@href = "?page=2"]').click()
        
        # Assertion
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)