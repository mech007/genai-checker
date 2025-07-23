# checkerapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile, MakerFormEntry

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.USER_TYPES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class MakerFormEntryForm(forms.ModelForm):
    class Meta:
        model = MakerFormEntry
        exclude = ['maker', 'submitted_at', 'ai_decision']

class MakerEntryForm(forms.ModelForm):
    class Meta:
        model = MakerFormEntry
        fields = [
            'customer_name', 'customer_account_number', 'currency',
            'beneficiary_name', 'beneficiary_account_number', 'branch_code'
        ]
        widgets = {
            'currency': forms.TextInput(attrs={'placeholder': 'USD, INR, etc.'}),
        }
