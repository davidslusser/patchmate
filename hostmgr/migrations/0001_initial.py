# Generated by Django 2.2.6 on 2019-12-08 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='date/time when this row was added')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='date/time when this row was updated')),
                ('active', models.BooleanField(default=True, help_text='select if this record is currently active')),
                ('name', models.CharField(help_text='name of this host', max_length=255, unique=True)),
                ('patching_enabled', models.BooleanField(default=False, help_text='enable/disable patching on this host')),
                ('last_patched_at', models.DateTimeField(blank=True, help_text='date/time when this host was last patched', null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
