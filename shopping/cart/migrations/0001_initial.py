# Generated by Django 3.1.7 on 2021-04-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=0)),
                ('quantity', models.PositiveIntegerField()),
                ('address', models.CharField(default='please add address', max_length=40)),
                ('product', models.ManyToManyField(to='product.Product')),
            ],
        ),
    ]
