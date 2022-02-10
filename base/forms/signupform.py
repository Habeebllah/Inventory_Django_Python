from base.models.customer import Customer
from django import forms
from django.db import transaction
from django.forms.utils import ValidationError
from base.models.users import *
from base.models.sales import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, PasswordResetForm
from django.forms import (formset_factory, modelformset_factory)


class SalesSignUpForm(UserCreationForm):


    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Username"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Surname"))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs=dict(required=True, max_length=30, placeholder='Last Name')), label=("First Name"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(
        required=True, max_length=30, render_value=False, placeholder='Enter Password')), label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(
        required=True, max_length=30, render_value=False, placeholder='Confirm Password')), label=("Confirm Password"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(
        required=True, max_lenght=50, placeholder='Enter Address')), label=("Email Address"))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs=dict(
        required=True, max_length=15, placeholder='+XXXXXXXXXXX')), label=("Phone Number"))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            ("The username already exists. Please try another one."))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # check and raise error if other user already exists with given email
        is_exists = User.objects.filter(email=email).exists()
        if is_exists:
            raise forms.ValidationError("User already exists with this email")
        return email

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    ("The two password fields did not match."))
        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_sales = True
        user.save()
        phonenumber = self.cleaned_data.get('phonenumber')
        Sales.objects.create(
            sales=user, phone_number=phonenumber)
        return user


class CustomerSignUpForm(UserCreationForm):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30, placeholder='Enter Your Username')),
                                label=("Username"), error_messages={'invalid': ("This value must contain only letters, numbers and underscores.")})
    first_name = forms.CharField(widget=forms.TextInput(
        attrs=dict(required=True, max_length=30, placeholder='First Name')), label=("Surname"))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs=dict(required=True, max_length=30, placeholder='Last Name')), label=("First Name"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(
        required=True, max_length=30, render_value=False, placeholder='Enter Password')), label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(
        required=True, max_length=30, render_value=False, placeholder='Confirm Password')), label=("Confirm Password"))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(
        required=True, max_lenght=50, placeholder='Enter Address')), label=("Email Address"))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs=dict(
        required=True, max_length=15, placeholder='+XXXXXXXXXXX')), label=("Phone Number"))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(
            ("The username already exists. Please try another one."))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # check and raise error if other user already exists with given email
        is_exists = User.objects.filter(email=email).exists()
        if is_exists:
            raise forms.ValidationError("User already exists with this email")
        return email

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    ("The two password fields did not match."))
        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        phonenumber = self.cleaned_data.get('phonenumber')
        Customer.objects.create(
            customer=user, phone_number=phonenumber)
        return user