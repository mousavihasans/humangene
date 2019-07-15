# Generated by Django 2.2.1 on 2019-07-15 05:27

from django.db import migrations, models
import django.utils.timezone
import genomequery.models
import utils.intenum


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenomeQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='genome query', max_length=200, unique=True)),
                ('price', models.IntegerField(default=2000000, help_text='unit is IRR.')),
                ('code', models.TextField(blank=True, null=True)),
                ('free_daily_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='QueryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', utils.intenum.IntEnumField(choices=[(0, 'free_daily'), (1, 'bought_by_credit'), (2, 'created_manually')], default=2, validators=[utils.intenum.IntEnumValidator(genomequery.models.QueryTypeChoices)])),
                ('response', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('performed_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
    ]
