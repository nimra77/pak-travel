# Generated by Django 4.2 on 2023-05-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_tour_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='destination_seasons',
            fields=[
                ('season_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]
