# Generated by Django 4.2 on 2023-05-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_city_hotels'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour_Type',
            fields=[
                ('tour_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]