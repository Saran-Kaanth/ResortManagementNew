# Generated by Django 4.2 on 2023-05-13 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_customuser_pincode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="pincode",
            field=models.IntegerField(default=""),
        ),
    ]