# Generated by Django 2.2.3 on 2020-03-16 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookhub', '0004_auto_20200316_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=4000)),
                ('photo', models.ImageField(blank=True, upload_to='recipe_images')),
                ('time', models.IntegerField(default=0)),
                ('averageRating', models.FloatField(default=0)),
                ('servings', models.IntegerField(default=0)),
                ('creationDate', models.DateTimeField()),
                ('views', models.IntegerField(default=0)),
                ('categories', models.ManyToManyField(to='cookhub.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookhub.UserModel')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('unit', models.CharField(max_length=20)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookhub.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('creationDate', models.DateField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookhub.Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookhub.UserModel')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookhub.Recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookhub.UserModel')),
            ],
            options={
                'unique_together': {('user', 'recipe')},
            },
        ),
    ]