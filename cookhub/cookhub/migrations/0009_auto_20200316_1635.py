# Generated by Django 2.2.3 on 2020-03-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookhub', '0008_auto_20200316_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='cookhub.Category'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='recipe_images'),
        ),
    ]