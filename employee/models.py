from django.db import models

# Create your models here.
class Emplist(models.Model):
    name = models.CharField(max_length=20)
    age = models.SmallIntegerField()
    birth = models.DateTimeField()
    gender = models.SmallIntegerField()
    salary = models.FloatField()
    hpic = models.ImageField(upload_to='pics')
    class Meta:
        db_table = 't_emplist'