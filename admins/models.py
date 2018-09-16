from django.db import models

# Create your models here.
class Admins(models.Model):
    username = models.CharField(max_length=20)
    realname = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    age = models.SmallIntegerField()
    gender = models.SmallIntegerField()
    birth = models.DateTimeField()
    hpic = models.ImageField(upload_to='pics')
    class Meta:
        db_table = 't_admin'
