# Generated by Django 5.1.1 on 2024-09-18 22:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0003_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='status_accepted',
            field=models.BooleanField(default=False, verbose_name='Статус лучшего ответа'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplication.answer', verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата обновления'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplication.question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Основная часть'),
        ),
    ]
