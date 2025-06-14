from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'expiry_month', 'expiry_year', 'cvc']
        widgets = {
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card number'}),
            'expiry_month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM'}),
            'expiry_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YY'}),
            'cvc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVC'}),
        }

class LoginForm(forms.Form):
    number = forms.CharField(required=True)

    def clean_number(self):
        number = self.cleaned_data['number']
        digits = re.sub(r'\D', '', number)

        if digits.startswith('998'):
            raise ValidationError("Номер не должен начинаться с 998")

        if not re.fullmatch(r'\d{9}', digits):
            raise ValidationError("Номер должен содержать 9 цифр, например, 90-7377720")

        # Например, список операторов:
        valid_prefixes = ['90', '91', '93', '94', '95', '97', '98', '99']
        if digits[:2] not in valid_prefixes:
            raise ValidationError("Номер должен начинаться с кода оператора, например 90")

        return digits