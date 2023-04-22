# Generated by Django 4.1.7 on 2023-04-22 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_honeypot', '0002_rename_honeypotsettings_honeypotsetting'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovementLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='ip address')),
                ('session_key', models.CharField(blank=True, max_length=50, null=True, verbose_name='session key')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='user-agent')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('path', models.TextField(blank=True, null=True, verbose_name='path')),
                ('previous_page', models.TextField(blank=True, null=True, verbose_name='previous page')),
            ],
            options={
                'verbose_name': 'movement log',
                'verbose_name_plural': 'movement logs',
                'ordering': ('timestamp',),
            },
        ),
    ]
