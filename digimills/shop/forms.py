from .models import Order, CustomerModel
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django import forms

class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username',]
        # fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control','autofocus':True}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User



class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True,'class':'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )  

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'class':'form-control','autofocus':True}), max_length=254)

class UserSetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
    )
class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    # mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        exclude = ['user','default_address']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','autofocus':True}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'house_number':forms.TextInput(attrs={'class':'form-control'}),
            'street':forms.NumberInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'district':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'})
        }


    


