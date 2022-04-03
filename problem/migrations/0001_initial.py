# Generated by Django 4.0.2 on 2022-03-20 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Описание проблемы')),
                ('description', models.TextField(blank=True, verbose_name='Подробное описание проблемы')),
                ('status', models.CharField(blank=True, choices=[(1, 'Новый'), (2, 'На рассмотрении'), (3, 'В работе'), (4, 'Не прошёл модерацию'), (5, 'Решена')], default=1, max_length=255, verbose_name='Статус')),
                ('is_draft', models.BooleanField(default=True, verbose_name='Черновик')),
            ],
            options={
                'verbose_name': 'Проблема',
                'verbose_name_plural': 'Проблемы',
            },
        ),
        migrations.CreateModel(
            name='ProblemAdditional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('description', models.TextField(verbose_name='Текст дополнения')),
                ('is_checked_applicant', models.BooleanField(default=False, verbose_name='Проверено заявителем')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименоввание')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.CharField(choices=[(1, 'Новый'), (2, 'На рассмотрении'), (3, 'В работе'), (4, 'Не прошёл модерацию'), (5, 'Решена')], max_length=255, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemLikeDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(1, 'За'), (2, 'Против')], max_length=255, verbose_name='Статус лайка, дизлайка')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255, verbose_name='Заголовок фотографии')),
                ('photo', models.ImageField(upload_to='images/problems', verbose_name='Изображение')),
                ('photo_small', models.ImageField(blank=True, upload_to='thumbs', verbose_name='Изображение thumb')),
                ('additional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.problemadditional', verbose_name='Дополнение к проблеме')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem', verbose_name='Проблема')),
            ],
        ),
    ]