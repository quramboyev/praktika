from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=19)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=2)
    cvc = models.CharField(max_length=3)
    added_at = models.DateTimeField(auto_now_add=True)

    def masked_number(self):
        # Возвращает номер карты с маской, например "**** **** **** 1234"
        return "**** **** **** " + self.card_number[-4:]

    def __str__(self):
        return f"{self.masked_number()} (User: {self.user.username})"