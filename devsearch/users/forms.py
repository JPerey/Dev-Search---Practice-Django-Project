from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):

    class Meta():
        ordering = [-1]
        model = User
        fields = ['first_name',
                  'email',
                  'username',
                  'password1',
                  'password2',
                  ]
        labels = {
            'first_name': 'Name',
        }
