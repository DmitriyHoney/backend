# Generated by Django 4.0.4 on 2022-05-24 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users/avatars', verbose_name='Аватар пользователя'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_small',
            field=models.ImageField(blank=True, upload_to='thumbs', verbose_name='Аватар пользователя thumb'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(auto_now_add=True, default='1990-06-20', verbose_name='Дата рождения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.CharField(blank=True, max_length=30, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('FEMALE', 'женский'), ('MALE', 'мужской')], default='MALE', max_length=10, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=30, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='user',
            name='marital_status',
            field=models.CharField(choices=[('MARRIED', 'замужем/женат'), ('SINGLE', 'холост/не замужем]')], default='SINGLE', max_length=55, verbose_name='Семейное положение'),
        ),
        migrations.AddField(
            model_name='user',
            name='middlename',
            field=models.CharField(blank=True, max_length=30, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='user_groups', to='auth.group', verbose_name='Группы пользователя'),
        ),
    ]
