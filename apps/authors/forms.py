import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.recipes import models
from utils.django_forms import field_attr


def validator_example(received_field):
    if True == False:
        raise ValidationError('This is an example')

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_attr(self.fields['password'], 'placeholder', 'Type your password here')
        field_attr(self.fields['password2'], 'placeholder', 'Type your password again')
        field_attr(self.fields['email'], 'placeholder', 'Type your email here')
        field_attr(self.fields['first_name'], 'placeholder', 'Ex: John')
        field_attr(self.fields['last_name'], 'placeholder', 'Ex: Doe')

    # Form fields

    password = forms.CharField(required=True, widget=forms.PasswordInput(), label='Password', validators=[validator_example])
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(), label='Repeat password')

    # Meta class for ModelForm

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Username',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username here'
            }),
            'email': forms.EmailInput(attrs={
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'required': True
            }),
        }
        error_messages = {
            'email': {
                'required': 'This field is required.'
            },
            'first_name': {
                'required': 'This field is required.'
            },
            'last_name': {
                'required': 'This field is required.'
            },
            'username': {
                'required': 'This field is required.'
            },
        }
    
    # Cleaning data

    def clean_password(self):
        data = self.cleaned_data.get('password', '')
        regex = re.compile('^(?!^\s)(.{8,32})?(?<!\s)$')

        if regex.match(data) == None:
            if len(data) < 8 or len(data) > 32:
                raise ValidationError('The password must be in a range of 8-32 characters')
            else:
                raise ValidationError('The password must contain only valid characters')
        
        # always return the data
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data['first_name'].strip()

        if len(data) < 3:
            raise ValidationError('This field is required (Min. 3 characters length).')

        return data
    
    def clean_last_name(self):
        data = self.cleaned_data['last_name'].strip()

        if len(data) < 3:
            raise ValidationError('This field is required (Min. 3 characters length).')

        return data
    
    def clean_email(self):
        data = self.cleaned_data['email'].strip()

        if not '@' in data:
            raise ValidationError('An email should contain a "@".')
        
        if User.objects.filter(email=data).exists():
            raise ValidationError('This email already exists.')

        return data
    
    def clean(self):
        data = super().clean()
        password = data.get('password', '')
        password2 = data.get('password2', '')

        if password and password2:
            if password != password2:
                raise ValidationError({
                    'password': 'Passwords must be equal.',
                    'password2': 'Passwords must be equal.'
                })

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_attr(self.fields['username'], 'placeholder', 'Type your username here')
        field_attr(self.fields['password'], 'placeholder', 'Type your password here')

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'required': True}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'required': True}))

class RecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['cover'].required = False

    class Meta:
        model = models.Recipe
        fields = ('title', 'description', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover')
        widgets = {
            'cover': forms.FileInput(
                attrs= {

                }
            ),
            'preparation_time_unit': forms.Select(
                choices= (('seconds', 'Seconds'), ('minutes', 'Minutes'), ('hours','Hours'))
            ),
            'servings_unit': forms.Select(
                choices= (('people', 'People'), ('portions', 'Portions'))
            ),
            'preparation_steps': forms.Textarea(
                attrs= {
                    'class': 'text-area'
                }
            )
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 3:
            raise ValidationError('Your title must have more than 3 characters.')

        return title