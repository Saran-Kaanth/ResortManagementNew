# Generated by Django 4.2 on 2023-05-13 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_customuser_pincode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="pincode",
            field=models.IntegerField(blank=True, default=""),
        ),
    ]
