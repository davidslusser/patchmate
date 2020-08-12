#!/usr/bin/env python

# import system modules
import sys
import os
import random
import environ
import django
import time, datetime
from django.core.exceptions import ValidationError

# setup django
sys.path.append(str(environ.Path(__file__) - 3))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patchmate.settings")
django.setup()
from rest_framework.authtoken.models import Token

# import models
from django.contrib.auth.models import (Group, User)
from servicemgr.models import (Owner, Service)
from hostmgr.models import (Host)
from patchmgr.models import (ServiceControl, PatchPool, PatchPoolRule, PatchSchedule, PackageWhitelist)


def get_random_row(queryset):
    """ return a single, random entry from a queryset """
    random_index = random.randint(0, queryset.count() - 1)
    return queryset[random_index]


def get_random_element(l):
    """ return a single, random element from a list """
    return random.choice(l)


def generate_user_data(count=1):
    """
    generate a list of dictionaries containing data necessary to create a User object
    :param count:
    :return:
    """
    return [{'username': 'user_{:03}'.format(i)} for i in range(1, count + 1)]


def generate_group_data(count=1):
    """
    generate a list of dictionaries containing data necessary to create a Group object
    :param count:
    :return:
    """
    return [{'name': 'group_{:03}'.format(i)} for i in range(1, count + 1)]


def generate_owner_data(count=1):
    """
    generate a list of dictionaries containing data necessary to create an Owner object
    :param count:
    :return:
    """
    return [{'name': 'owner_{:03}'.format(i), 'group': get_random_row(Group.objects.all())}
            for i in range(1, count + 1)]


def generate_service_data(count=1):
    """
    generate a list of dictionaries containing data necessary to create an Service object
    :param count:
    :return:
    """
    service_name_list = ['ansible', 'ant', 'apache', 'auth', 'backup', 'bower', 'bucket', 'build', 'cache', 'calico',
                         'cert', 'chef', 'compute', 'content', 'convert', 'couch', 'dashboard', 'db', 'deploy', 'dns',
                         'docker', 'download', 'elastic', 'elk', 'file', 'gerrit', 'git', 'iaas', 'infra', 'ipam',
                         'jenkins', 'jira', 'jump', 'kafka', 'kube', 'ldap', 'license', 'log', 'maven', 'mongo',
                         'mysql', 'nagios', 'net', 'nginx', 'npm', 'ntp', 'paas', 'packer', 'patch', 'postgress',
                         'proxy', 'puppet', 'redis', 'repo', 'rmq', 'rpm', 'salt', 'scm', 'search', 'sensu', 'splunk',
                         'storage', 'temp', 'terraform', 'test', 'travis', 'upload', 'vagrant', 'vault', 'vpn', 'web',
                         'zookeeper']

    return [{'name': random.choice(service_name_list),
             'owner': get_random_row(Owner.objects.all()),
             }
            for i in range(1, count + 1)]


def create_users(data=None, clean=False, count=1):
    """
    Create user objects
    :param data:
    :param clean:
    :param count:
    :return:
    """

    if clean:
        User.objects.filter(is_superuser=False).delete()
    if not data:
        data = generate_user_data(count=count)
    for obj in data:
        user, is_new = User.objects.get_or_create(**obj)
        if is_new:
            Token.objects.get_or_create(user=user)


def create_groups(data=None, clean=False, count=1):
    """
    Create group objects
    :param data:
    :param clean:
    :param count:
    :return:
    """
    if clean:
        Group.objects.all().delete()
    if not data:
        data = generate_group_data(count=count)
    for obj in data:
        group = Group.objects.get_or_create(name=obj['name'], defaults=obj)[0]

        # add some users to group
        for i in range(0, random.randint(0, 5)):
            group.user_set.add(get_random_row(User.objects.all()))


def create_owners(data=None, clean=False, count=1):
    """
    create Owner objects
    :param data:
    :param clean:
    :param count:
    :return:
    """
    if clean:
        Owner.objects.all().delete()
    if not data:
        data = generate_owner_data(count=count)
    for obj in data:
        Owner.objects.get_or_create(name=obj['name'], defaults=obj)


def create_services(data=None, clean=False, count=1):
    """
    create Service objects
    :param data:
    :param clean:
    :param count:
    :return:
    """
    patch_frequency_list = [15, 30, 45, 60, 90]
    dc_list = ['sfo', 'lax', 'rno']
    day_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    package_name_list = ['python', 'mysql', 'perl', 'php', 'zip', 'openssh', 'gnome', 'grep', 'glib', 'libxml',
                         'httpd', 'nginx']

    if clean:
        Service.objects.all().delete()
    if not data:
        data = generate_service_data(count=count)
    for obj in data:
        service, is_new = Service.objects.get_or_create(name=obj['name'], defaults=obj)
        if is_new:
            # create service control object
            ServiceControl.objects.get_or_create(service=service,
                                                 patch_frequency=random.choice(patch_frequency_list),
                                                 patching_enabled=bool(random.getrandbits(1)),
                                                 )

            # create a random number of hosts for service
            for i in range(1, random.randint(2, 15)):
                Host.objects.get_or_create(name="{}_{}_{:03}".format(service.name, random.choice(dc_list), i),
                                           service=service,
                                           patching_enabled=bool(random.getrandbits(1))
                                           )

            # create patch pools for this service
            for dc in dc_list:
                pool, is_new = PatchPool.objects.get_or_create(
                    service=service,
                    name="{}_{}".format(service, dc),
                    description="patching pool for {} hosts in the {} datacenter".format(service, dc),
                    hostname_regex="^({})_{}_(/d{{3}})$".format(service.name, dc),
                    patching_enabled=bool(random.getrandbits(1)),
                )

                # create patching rule(s) for pool
                rule, is_new = PatchPoolRule.objects.get_or_create(
                    pool=pool,
                    name="patching rule for {}".format(pool.name),
                    patching_enabled=bool(random.getrandbits(1)),
                    min_percent_in_service=random.randint(0, 40),
                    max_percent_out_of_service=random.randint(0, 40),
                    max_percent_daily_patch=random.randint(0, 40),
                )

                # create patching schedule(s) for pool
                schedule, is_new = PatchSchedule.objects.get_or_create(
                    pool=pool,
                    name="schedule for host patching in {}".format(pool.name),
                    patching_enabled=bool(random.getrandbits(1)),
                    start_day=random.choice(day_list),
                    end_day=random.choice(day_list),
                    start_hour=random.randint(0, 24),
                    end_hour=random.randint(0, 24),
                    start_minute=random.randint(0, 60),
                    end_minute=random.randint(0, 60),
                )

                # add some package whitelist entries
                for i in range(random.randint(1, 6)):
                    package = random.choice(package_name_list)
                    wl, is_new = PackageWhitelist.objects.get_or_create(
                        service=service,
                        name=package,
                        package_regex="{}*".format(package),
                    )


def create_core(clean=False):
    """ create core records required (users, groups, etc.) """
    create_users(clean=clean, count=4)
    create_groups(clean=clean, count=12)


def create_servicemgr_entries(clean=False):
    create_owners(clean=clean, count=8)
    create_services(clean=clean, count=8)


def create_patchmgr_entries():
    pass


def create_all():
    """ create all the things """
    create_core()
    create_servicemgr_entries()


def main():
    """ script entry point """
    print('Starting local dev data creation')
    create_all()
    print('Done!')


if __name__ == "__main__":
    sys.exit(main())