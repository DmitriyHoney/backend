# Generated by Django 4.0.4 on 2022-05-24 08:09

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True, verbose_name='Телефон'),
        ),
    ]
