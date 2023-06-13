# Generated by Django 4.2 on 2023-05-23 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour_Packages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('package_name', models.CharField(default='', max_length=122)),
                ('tour_length', models.TextField(blank=True, max_length=100)),
                ('rupees', models.TextField(blank=True, max_length=100)),
                ('destinations', models.TextField(blank=True, max_length=150)),
                ('age', models.TextField(blank=True, max_length=100)),
                ('tour_companies_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.tour_companies')),
            ],
        ),
    ]