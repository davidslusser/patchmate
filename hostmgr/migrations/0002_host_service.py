# Generated by Django 2.2.6 on 2019-12-08 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hostmgr', '0001_initial'),
        ('servicemgr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicemgr.Service'),
        ),
    ]
