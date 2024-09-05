from django import forms
from .models import TotalCost

class TotalCostForm(forms.ModelForm):
    class Meta:
        model = TotalCost
        fields = [
            'u21', 'ru21', 'u22', 'ru22', 'u23', 'ru23', 'u24', 'ru24', 'u25', 'ru25', 'u26', 'ru26',
            'u31', 'ru31', 'u32', 'ru32', 'u33', 'ru33', 'u34', 'ru34', 'u35', 'ru35','u37','ru37',
            'u41', 'ru41','u43', 'ru43', 'u44', 'ru44',
            'u51', 'ru51', 'u52', 'ru52','u57', 'ru57', 'u58', 'ru58',
            'u61', 'ru61','u63', 'ru63', 'u64', 'ru64', 'u65', 'ru65',
            'u71', 'ru71', 'u72', 'ru72', 'u73', 'ru73', 'u74', 'ru74',
            'u81', 'ru81', 'u82', 'ru82', 'u83', 'ru83', 'u84', 'ru84',
            'u91', 'ru91', 'u92', 'ru92', 'u93', 'ru93', 'u94', 'ru94', 'u95', 'ru95', 'u96', 'ru96', 'u97', 'ru97',
            'ru1a','ru1c','ru1d','ru1e',
            'ru2a','ru2b','ru2d','ru2e','ru2f',
            'ru3b','ru3c','ru3d',
            'ru4a','ru4b'
        ]


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)