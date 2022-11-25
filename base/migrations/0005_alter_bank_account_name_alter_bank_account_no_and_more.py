# Generated by Django 4.1.3 on 2022-11-23 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_full_name_bank_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='account_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='bank',
            name='account_no',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='bank',
            name='bank_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='bank',
            name='routing_no',
            field=models.CharField(default='', max_length=30),
        ),
    ]