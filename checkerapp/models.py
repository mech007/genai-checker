# checkerapp/models.py
from django.db import models
from django.contrib.auth.models import User

class MakerFormEntry(models.Model):
    maker = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    customer_name = models.CharField(max_length=255)
    customer_account_number = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    beneficiary_name = models.CharField(max_length=255)
    beneficiary_account_number = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=20)

    ai_decision = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.beneficiary_name}"

