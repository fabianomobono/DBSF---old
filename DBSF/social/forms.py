from django import forms
CHOICES = {('male', 'female', 'other')}
class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', max_length=40, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))


class RegisterForm(forms.Form):
    First_name = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    Last_name = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(label='', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(label='', max_length=40, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password_confirmation = forms.CharField(label='', max_length=40, widget=forms.PasswordInput(attrs={'placeholder':'Confirmation'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder':'Date of Birth'}))
