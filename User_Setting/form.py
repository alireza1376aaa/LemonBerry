from django import forms
from django.core.exceptions import ValidationError


class Register_form(forms.Form):
    username = forms.RegexField(
        widget=forms.TextInput(attrs={'placeholder': 'Add Username', 'class': 'form-control', 'id': 'form_w_75'}),
        required=True, error_messages={'required': 'Add username', 'invalid': 'you can use '},
        regex='^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$')

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Add Email address', 'class': 'form-control', 'id': 'form_w_75'}),
        required=True, error_messages={'required': 'Add Email'})
    Password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Add Password', 'class': 'form-control', 'id': 'form_w_75'}),
        required=True, error_messages={'required': 'Add Password'})

    Password_again = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Add again Password', 'class': 'form-control', 'id': 'form_w_75'}),
        required=True, error_messages={'required': 'Add Password'})

    def clean_Password_again(self):

        mypass = self.cleaned_data['Password']
        newpass = self.cleaned_data['Password_again']

        if mypass == newpass:
            return newpass
        else:
            raise ValidationError('in not corect password')


class log_in_form(forms.Form):
    usernameoremail = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Add Email or username', 'class': 'form-control', 'id': 'form_w_75'}),
        required=True, error_messages={'required': 'Put your Email or Username'})

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'add Password', 'class': 'form-control', 'id': 'form_w_75'}),
        required=True, error_messages={'required': 'Put your Password'})


class password_form(forms.Form):
    Password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Add new Password', 'class': 'form-control'}),
        required=True, error_messages={'required': 'Add Password'})

    Password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Add again Password', 'class': 'form-control'}),
        required=True, error_messages={'required': 'Add Password'})
