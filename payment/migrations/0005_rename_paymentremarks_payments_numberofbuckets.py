# Generated by Django 3.2.6 on 2021-09-10 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20210910_0843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payments',
            old_name='paymentRemarks',
            new_name='numberOfBuckets',
        ),
    ]
