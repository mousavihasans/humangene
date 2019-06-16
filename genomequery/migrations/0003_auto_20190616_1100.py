# Generated by Django 2.2.1 on 2019-06-16 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genomequery', '0002_auto_20190614_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenomeQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='genome query', max_length=200, unique=True)),
                ('price', models.IntegerField(default=2000000, help_text='unit is IRR.')),
                ('code', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='queryitem',
            name='code',
        ),
        migrations.RemoveField(
            model_name='queryitem',
            name='name',
        ),
        migrations.RemoveField(
            model_name='queryitem',
            name='price',
        ),
        migrations.AddField(
            model_name='queryitem',
            name='genome_query',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='genomequery.GenomeQuery'),
            preserve_default=False,
        ),
    ]
