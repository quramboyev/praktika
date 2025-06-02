from django import forms
from django.core.exceptions import ValidationError
import re

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