from django.db import models

# Create your models here.
class tbl_Studentmarks(models.Model):
    name = models.CharField(max_length=50)
    student_class = models.CharField(max_length=50)

    sub1 = models.IntegerField()
    sub2 = models.IntegerField()
    sub3 = models.IntegerField()
    sub4 = models.IntegerField()
    sub5 = models.IntegerField()
    sub6 = models.IntegerField()
    sub7 = models.IntegerField()

    total = models.IntegerField()
    percentage = models.IntegerField()

    def __str__(self):
            return self.name