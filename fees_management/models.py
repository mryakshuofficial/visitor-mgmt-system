from django.db import models


# Create your models here.

class FeePayment(models.Model):
    student_name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    email = models.EmailField()

    village = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    payment_id = models.CharField(max_length=100, unique=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - ₹{self.amount} - {'Paid' if self.is_paid else 'Unpaid'}"