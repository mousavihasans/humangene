# Generated by Django 2.2.1 on 2019-06-14 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('genomequery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queryitem',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='queryitem',
            name='performed_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='queryitem',
            name='performed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='performed_queries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='queryitem',
            name='code',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='queryitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_queries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='queryitem',
            name='name',
            field=models.CharField(default='genome query', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='queryitem',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
    ]