from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=255,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    # Check for entered email to be unique
    def clean_email(self):
        entered_email = self.cleaned_data.get('email')
        if User.objects.filter(email=entered_email).exists():
            raise forms.ValidationError("This email is already been registered !")
        return entered_email 

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last name'


class ProfileForm(forms.ModelForm):    
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'bio', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.attrs['class'] = 'form-control'
        self.fields['birth_date'].widget.attrs['placeholder'] = 'Birth date, Example : (2002-02-03)'
        self.fields['bio'].widget.attrs['class'] = 'form-control'
        self.fields['bio'].widget.attrs['placeholder'] = 'Tell to the world who you really are !'
        self.fields['profile_image'].widget.attrs['class'] = 'form-control'
