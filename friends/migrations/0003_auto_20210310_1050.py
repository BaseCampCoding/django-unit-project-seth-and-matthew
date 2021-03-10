# Generated by Django 3.1.7 on 2021-03-10 16:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friends', '0002_auto_20210310_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendlist',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]