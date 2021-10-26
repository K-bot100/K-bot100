# Generated by Django 3.2.6 on 2021-09-10 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20210910_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payments',
            old_name='amount',
            new_name='amountPaid',
        ),
        migrations.RenameField(
            model_name='payments',
            old_name='comm',
            new_name='community',
        ),
        migrations.RenameField(
            model_name='payments',
            old_name='payermessage',
            new_name='paymentRemarks',
        ),
        migrations.RenameField(
            model_name='payments',
            old_name='phonepartyid',
            new_name='phoneNumber',
        ),
        migrations.RenameField(
            model_name='payments',
            old_name='ptype',
            new_name='productType',
        ),
        migrations.RenameField(
            model_name='payments',
            old_name='fintransid',
            new_name='transactionId',
        ),
    ]