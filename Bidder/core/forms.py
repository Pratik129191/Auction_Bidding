from django.forms import DateInput

from .models import User
from .tests import calculate_age
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class CustomRegisterForm(BaseUserCreationForm):
    email = forms.EmailField()
    # birth_date = forms.DateField(widget=DateInput(format='%y-%m-%d'))
    address = forms.CharField(widget=forms.TextInput(attrs={'size': 80}))

    def save(self, commit=True):
        self.instance = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password2'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            birth_date=self.cleaned_data['birth_date'],
            address=self.cleaned_data['address'],
        )
        return self.instance

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'username', 'email', 'password1', 'password2',
            'phone', 'birth_date', 'age',
            'address'
        ]
        # widgets = {
        #     'sex': forms.Select(attrs={'style': 'width:540px; height: 35px'})
        # }

