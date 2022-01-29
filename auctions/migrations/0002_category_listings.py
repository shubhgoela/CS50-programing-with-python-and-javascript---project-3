# Generated by Django 4.0 on 2022-01-20 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True)),
                ('image', models.URLField(max_length=1000)),
                ('status', models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('BID', 'BIDDING'), ('CLOSED', 'CLOSE')], default='ACTIVE', max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.user')),
            ],
        ),
    ]
