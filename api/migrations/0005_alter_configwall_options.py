# Generated by Django 4.2.1 on 2023-05-25 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_configwall_conf'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configwall',
            options={'ordering': ['-created']},
        ),
    ]
