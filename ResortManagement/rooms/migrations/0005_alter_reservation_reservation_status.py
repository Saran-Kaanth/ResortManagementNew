# Generated by Django 4.2 on 2023-04-30 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0004_remove_reservation_status_reservation_payment_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="reservation_status",
            field=models.CharField(
                default="Reserved", max_length=254, verbose_name="Reservation Status"
            ),
        ),
    ]