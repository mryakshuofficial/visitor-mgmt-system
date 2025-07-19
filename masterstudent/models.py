# masterstudent/models.py

from django.db import models

class MasterStudent(models.Model):
    gr_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    student_class = models.CharField(max_length=20, blank=True, null=True)
    fname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    aadhar = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    photo_path = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.gr_no} - {self.name}"
