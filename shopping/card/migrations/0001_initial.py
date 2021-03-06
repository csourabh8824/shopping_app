# Generated by Django 3.1.7 on 2021-04-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_on_card', models.CharField(max_length=20)),
                ('card_type', models.CharField(choices=[('CREDIT CARD', 'Credit card'), ('DEBIT CARD', 'Debit card')], max_length=20)),
                ('expiration', models.CharField(max_length=10)),
            ],
        ),
    ]
