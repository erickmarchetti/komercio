# Generated by Django 4.1.2 on 2022-10-18 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="user",
            new_name="seller",
        ),
    ]
