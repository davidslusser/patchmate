# Generated by Django 2.2.6 on 2019-12-09 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patchmgr', '0003_auto_20191208_2307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patchpoolrule',
            old_name='enabled',
            new_name='patching_enabled',
        ),
        migrations.RemoveField(
            model_name='patchpoolrule',
            name='max_count_oos',
        ),
        migrations.RemoveField(
            model_name='patchpoolrule',
            name='max_daily_percent',
        ),
        migrations.RemoveField(
            model_name='patchpoolrule',
            name='max_percent_oos',
        ),
        migrations.RemoveField(
            model_name='patchpoolrule',
            name='min_count_is',
        ),
        migrations.AddField(
            model_name='patchpoolrule',
            name='max_percent_daily_patch',
            field=models.FloatField(default=10, help_text='percent of hosts in this pool that can be patched in a single day'),
        ),
        migrations.AddField(
            model_name='patchpoolrule',
            name='max_percent_out_of_service',
            field=models.FloatField(default=10, help_text='percent of hosts in this pool that can be out of service'),
        ),
        migrations.AddField(
            model_name='patchpoolrule',
            name='min_percent_in_service',
            field=models.FloatField(default=0, help_text='percent of hosts in this pool that must remain in service'),
        ),
        migrations.AddField(
            model_name='servicecontrol',
            name='max_percent_daily_patch',
            field=models.FloatField(default=10, help_text='percent of hosts that can be patched in a single day'),
        ),
        migrations.AddField(
            model_name='servicecontrol',
            name='max_percent_out_of_service',
            field=models.FloatField(default=10, help_text='percent of hosts in this service that can be out of service'),
        ),
        migrations.AddField(
            model_name='servicecontrol',
            name='min_percent_in_service',
            field=models.FloatField(default=0, help_text='percent of hosts in this service that must remain in service'),
        ),
    ]
