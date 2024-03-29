# Generated by Django 2.2.1 on 2019-10-25 17:55

import ckeditor.fields
import cms.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.intenum


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20191020_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', utils.intenum.IntEnumField(choices=[(0, 'page'), (1, 'news')], default=0, validators=[utils.intenum.IntEnumValidator(cms.models.ContentTypeChoices)])),
                ('title_fa', models.CharField(max_length=500)),
                ('title_en', models.CharField(default='', max_length=500)),
                ('text_fa', ckeditor.fields.RichTextField()),
                ('text_en', ckeditor.fields.RichTextField(default='')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/posts')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cms.Category')),
                ('tags', models.ManyToManyField(blank=True, to='cms.Tag')),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='category',
        ),
        migrations.RemoveField(
            model_name='page',
            name='tags',
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
