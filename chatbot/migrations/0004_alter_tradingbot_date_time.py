# Generated by Django 4.2 on 2023-05-05 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_tradingbot_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradingbot',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]