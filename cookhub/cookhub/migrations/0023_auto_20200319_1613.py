# Generated by Django 2.2.3 on 2020-03-19 16:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cookhub', '0022_auto_20200319_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='creationDate',
            field=models.DateField(blank=True, default=datetime.datetime(2020, 3, 19, 16, 13, 25, 687681, tzinfo=utc)),
        ),
    ]