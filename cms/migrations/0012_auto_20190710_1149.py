# Generated by Django 2.2.1 on 2019-07-10 07:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20190707_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='slideritem',
            name='description',
            field=models.CharField(default='Description Text', max_length=500),
            preserve_default=False,
        ),
    ]
