# Generated by Django 4.0 on 2022-01-21 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bids_user_alter_listings_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='user',
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_bids', to='auctions.user'),
        ),
        migrations.RemoveField(
            model_name='listings',
            name='category',
        ),
        migrations.AddField(
            model_name='listings',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat_listings', to='auctions.category'),
        ),
        migrations.RemoveField(
            model_name='listings',
            name='user',
        ),
        migrations.AddField(
            model_name='listings',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.user'),
        ),
    ]
