# Generated by Django 5.1.2 on 2024-12-25 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('publisher', models.CharField(max_length=255)),
                ('publish_year', models.IntegerField()),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('classification_number', models.FloatField()),
                ('classification', models.CharField(max_length=50)),
            ],
        ),
    ]
