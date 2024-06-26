# Generated by Django 5.0.3 on 2024-03-29 09:19

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_hotel_like_count_hotellike'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.booking')),
            ],
        ),
    ]
