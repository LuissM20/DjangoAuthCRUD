# Generated by Django 5.0.6 on 2024-05-13 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='desciption',
            new_name='description',
        ),
    ]
