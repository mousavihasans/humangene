# Generated by Django 2.2.1 on 2019-10-20 19:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='increasecreditviabank',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
