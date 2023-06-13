# Generated by Django 4.2 on 2023-05-23 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction_Places',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(default='', max_length=122)),
                ('Place_name', models.CharField(max_length=122)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('long_description', models.TextField(max_length=1500)),
                ('Image', models.ImageField(upload_to='pics')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(default='', max_length=122)),
                ('province', models.CharField(max_length=122)),
                ('hotels', models.IntegerField(default=0)),
                ('area', models.CharField(max_length=100)),
                ('population', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('long_description', models.TextField(max_length=1500)),
                ('Image', models.ImageField(upload_to='pics')),
                ('No_of_attrac_places', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tour_Companies',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(default='', max_length=122)),
                ('address', models.TextField(blank=True, max_length=100)),
                ('response_time', models.TextField(blank=True, max_length=50)),
                ('group_size', models.TextField(blank=True, max_length=50)),
                ('adventure_styles', models.TextField(blank=True, max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Review_Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('review', models.TextField(blank=True, max_length=500)),
                ('rating', models.FloatField()),
                ('sentiment', models.FloatField(blank=True, null=True)),
                ('attraction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.attraction_places')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='attraction_places',
            name='city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.city'),
        ),
    ]
