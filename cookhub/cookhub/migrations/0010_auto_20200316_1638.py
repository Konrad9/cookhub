# Generated by Django 2.2.3 on 2020-03-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookhub', '0009_auto_20200316_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(blank=True, to='cookhub.Category'),
        ),
    ]
