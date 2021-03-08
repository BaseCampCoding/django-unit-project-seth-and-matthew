# Generated by Django 3.1.7 on 2021-03-08 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('correct_answer', models.CharField(max_length=120)),
                ('description', models.TextField()),
            ],
        ),
    ]
