# Generated by Django 4.0 on 2022-01-21 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bids_listing_alter_comments_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='listing',
        ),
        migrations.AddField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listings'),
        ),
        migrations.RemoveField(
            model_name='comments',
            name='listing',
        ),
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listings'),
        ),
    ]
