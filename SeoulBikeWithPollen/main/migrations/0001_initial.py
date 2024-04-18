# Generated by Django 5.0.4 on 2024-04-17 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeoulBikeStationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_id', models.CharField(max_length=20, verbose_name='대여소 ID')),
                ('station_name', models.CharField(max_length=100, verbose_name='대여소 이름')),
                ('raccnt', models.IntegerField(verbose_name='거치대 수')),
                ('addr1', models.CharField(max_length=20, verbose_name='구')),
                ('addr2', models.CharField(max_length=20, verbose_name='동')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SeoulBikeStationNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bikecnt', models.IntegerField(default=0, verbose_name='자전거 수')),
                ('bikeratio', models.IntegerField(verbose_name='거치율')),
                ('station', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='now', to='main.seoulbikestationinfo')),
            ],
        ),
    ]