# Generated by Django 4.1 on 2022-08-23 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0002_myuser"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MyUser",
        ),
    ]
