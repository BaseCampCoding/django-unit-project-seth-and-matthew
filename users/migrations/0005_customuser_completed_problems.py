# Generated by Django 3.1.7 on 2021-03-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210310_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='completed_problems',
            field=models.CharField(default='', max_length=200),
        ),
    ]
