# Generated by Django 2.2.6 on 2019-12-08 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='date/time when this row was added')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='date/time when this row was updated')),
                ('active', models.BooleanField(default=True, help_text='select if this record is currently active')),
                ('name', models.CharField(help_text='name of this group', max_length=32, unique=True)),
                ('email', models.EmailField(blank=True, help_text='group email alias for group', max_length=254, null=True)),
                ('group', models.ForeignKey(help_text='group this owner belongs to', on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='date/time when this row was added')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='date/time when this row was updated')),
                ('active', models.BooleanField(default=True, help_text='select if this record is currently active')),
                ('name', models.CharField(help_text='name of this service', max_length=255, unique=True)),
                ('description', models.CharField(blank=True, help_text='description of this service', max_length=255, null=True)),
                ('patching_enabled', models.BooleanField(default=False, help_text='enable/disable patching on this service')),
                ('script_path', models.CharField(default='/opt/patchmate/service_control_scripts', help_text='location on hosts where service control scripts live', max_length=64)),
                ('patch_frequency', models.IntegerField(default=60, help_text='frequency, in days, of how often patch events should take place')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicemgr.Owner')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
