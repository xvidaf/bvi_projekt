# Generated by Django 4.1.7 on 2023-03-25 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_honeypot', '0002_auto_20160208_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginattempt',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='password'),
        ),
    ]
