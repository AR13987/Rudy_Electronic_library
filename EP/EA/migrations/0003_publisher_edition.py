# Generated by Django 5.1.3 on 2024-11-23 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EA', '0002_author_biography_author_notable_achievements_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='EA.book')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EA.publisher')),
            ],
            options={
                'unique_together': {('book', 'publisher', 'year')},
            },
        ),
    ]