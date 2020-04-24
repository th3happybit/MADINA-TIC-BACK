from django.contrib.auth.models import Group
new_group, created = Group.objects.get_or_create(name='clients')
new_group, created = Group.objects.get_or_create(name='admins')
new_group, created = Group.objects.get_or_create(name='maires')
new_group, created = Group.objects.get_or_create(name='services')