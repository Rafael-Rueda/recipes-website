from authors.forms import RegisterForm
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from apps.recipes.tests.fixtures.recipes_base_tests import TestBase


class RegisterPageTest(TestCase):

    @parameterized.expand([
        ('username', 'Type your username here'),
        ('password', 'Type your password here'),
        ('password2', 'Type your password again'),
        ('first_name', 'Ex: John'),
        ('last_name', 'Ex: Doe'),
        ('email', 'Type your email here'),
    ])
    def test_fields_placeholder_are_correct(self, field, expected_placeholder):
        form = RegisterForm()
        current_placeholder = form.fields.get(field).widget.attrs['placeholder']

        self.assertEqual(current_placeholder, expected_placeholder)

    @parameterized.expand([
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Repeat password'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'Email address'),
    ])
    def test_fields_label_are_correct(self, field, expected_label):
        form = RegisterForm()
        current_label = form.fields.get(field).label
        
        self.assertEqual(current_label, expected_label)

    def test_if_no_post_template_rendered_is_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'global/pages/404.html')

class RegisterPageFormTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'User',
            'first_name': 'User',
            'last_name': 'User',
            'email': 'user@email.com',
            'password': 'P4ssword',
            'password2': 'P4ssword',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This field is required.'),
        ('first_name', 'This field is required (Min. 3 characters length).'),
        ('last_name', 'This field is required (Min. 3 characters length).'),
        ('email', 'An email should contain a'),
        ('password', 'This field is required.'),
        ('password2', 'This field is required.'),
    ])
    def test_if_username_field_is_invalid_when_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_if_password_and_password2_must_be_equal(self):
        self.form_data['password2'] = 'P4ss'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn('Passwords must be equal.', response.content.decode('utf-8'))

    def test_if_email_cannot_be_a_duplicated_one(self):
        url = reverse('authors:create')
        response_1 = self.client.post(url, data=self.form_data, follow=True)

        self.form_data['username'] = 'User2'
        response_2 = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn('User created with success', response_1.content.decode('utf-8'))
        self.assertIn('This email already exists.', response_2.content.decode('utf-8'))

class LoginPageTest(TestCase):
    def test_test(self):
        ...


class LogoutTest(TestBase):
    def test_if_a_user_can_be_logged_out(self):
        self._make_user(username='user', password='pass')
        self.client.login(username='user', password='pass')

        response = self.client.post(path=reverse('authors:logout'), follow=True)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), 'User logged-out with success.')
