# Generated by Django 4.0 on 2024-08-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default=1, upload_to='', verbose_name='Аватар'),
            preserve_default=False,
        ),
    ]
