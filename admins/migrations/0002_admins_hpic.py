# Generated by Django 2.0.2 on 2018-08-15 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admins',
            name='hpic',
            field=models.ImageField(default='text.jpg', upload_to='pics'),
        ),
    ]
