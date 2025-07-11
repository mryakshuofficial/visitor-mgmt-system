from django.db import models

# Create your models here.
class tbl_Visitors(models.Model):
    name = models.CharField(max_length=50)
    visiting_whom = models.CharField(max_length=50)
    purpose = models.TextField()
    in_time = models.DateField()
    out_time = models.DateField(blank=True ,null=True )

    def __str__(self):
        return self.name
    