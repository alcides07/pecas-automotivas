# Generated by Django 5.1.6 on 2025-02-11 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_number', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('details', models.TextField(max_length=555)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.PositiveIntegerField()),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
                ('parts', models.ManyToManyField(blank=True, related_name='parts', to='api.part')),
            ],
        ),
    ]
