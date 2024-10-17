from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    """
    Extends UserCreationForm to include email.
    """
    email = forms.EmailField(max_length=254, required=True,
    help_text='Required. Enter a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )