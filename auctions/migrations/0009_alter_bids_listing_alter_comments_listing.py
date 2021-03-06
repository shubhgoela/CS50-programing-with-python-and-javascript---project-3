# Generated by Django 4.0 on 2022-01-21 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='listing',
            field=models.ManyToManyField(related_name='bids', to='auctions.Listings'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='listing',
            field=models.ManyToManyField(related_name='comments', to='auctions.Listings'),
        ),
    ]
