# Generated by Django 3.0.3 on 2020-02-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200226_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repayments',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='repaymentuploads',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seasons',
            name='EndDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='seasons',
            name='StartDate',
            field=models.DateField(blank=True),
        ),
    ]