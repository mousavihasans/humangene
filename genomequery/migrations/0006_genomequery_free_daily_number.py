# Generated by Django 2.2.1 on 2019-06-16 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genomequery', '0005_auto_20190616_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='genomequery',
            name='free_daily_number',
            field=models.IntegerField(default=0),
        ),
    ]