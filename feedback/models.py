from django.db import models
from masterstudent.models import MasterStudent  # or your actual path


class Feedback(models.Model):
    student = models.ForeignKey(MasterStudent, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback #{self.id} - {self.submitted_at.strftime('%d-%m-%Y %H:%M')}"