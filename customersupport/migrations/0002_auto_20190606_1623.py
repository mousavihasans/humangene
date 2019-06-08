# Generated by Django 2.2.1 on 2019-06-06 16:23

import customersupport.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.intenum


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customersupport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('state', utils.intenum.IntEnumField(choices=[(0, 'accepted'), (1, 'in_progress'), (2, 'completed_with_errors'), (3, 'completed_successfully')], default=0, validators=[utils.intenum.IntEnumValidator(customersupport.models.TaskStateChoices)])),
                ('result', models.FileField(blank=True, null=True, upload_to='files/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('uploaded_result_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='TrackTasks',
        ),
    ]
