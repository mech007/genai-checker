# checkerapp/forms.py
from django import forms
from .models import MakerFormEntry

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
