# Generated by Django 5.1.4 on 2025-01-03 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavigationSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin_url', models.URLField(blank=True, verbose_name='LinkedIn URL')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub URL')),
                ('mastodon_url', models.URLField(blank=True, verbose_name='Mastodon URL')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
