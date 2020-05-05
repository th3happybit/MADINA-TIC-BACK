from django.contrib.auth.models import Permission, ContentType
from django.contrib.auth.models import Group
"""
codenames:
'add_announce'
'change_announce'
'delete_announce'
'view_announce'
'add_declaration'
'change_declaration'
'delete_declaration'
'view_declaration'
'add_declarationcomplementdemand'
'change_declarationcomplementdemand'
'delete_declarationcomplementdemand'
'view_declarationcomplementdemand'
'add_declarationrejection'
'change_declarationrejection'
'delete_declarationrejection'
'view_declarationrejection'
'add_declarationtype'
'change_declarationtype'
'delete_declarationtype'
'view_declarationtype'
'add_document'
'change_document'
'delete_document'
'view_document'
'add_report'
'change_report'
'delete_report'
'view_report'
'add_reportcomplementdemand'
'change_reportcomplementdemand'
'delete_reportcomplementdemand'
'view_reportcomplementdemand'
'add_reportrejection'
'change_reportrejection'
'delete_reportrejection'
'view_reportrejection'
'add_user'
'change_user'
'delete_user'
'view_user'
"""
# add permissions from comment in top to the lists below depend on the role permissions
clients = ['add_declaration', 'change_declaration', 'view_declaration', 'delete_declaration', 'view_declarationcomplementdemand', 'add_document', 'change_document', 'delete_document', 'view_document', ]
maires = ['view_declaration', 'add_declarationcomplementdemand','change_declarationcomplementdemand', 'view_declarationcomplementdemand', 'delete_declarationcomplementdemand']
services = []

clients_group = Group.objects.get(name='clients')
maires_group = Group.objects.get(name='maires')
services_group = Group.objects.get(name='services')

def get_perms(codenames, model):
	content_type = ContentType.objects.get(app_label='api', model=model)
	perms = Permission.objects.filter(content_type=content_type)
	dperms = []
	for p in perms:
		if p.codename in codenames:
			dperms.append(p)
	return dperms

models = ['announce', 'declaration', 'declarationcomplementdemand', 'declarationrejection', 'declarationtype', 'document', 'report', 'reportcomplementdemand', 'reportrejection', 'user']

for model in models:
	aperms = get_perms(clients, model)
	for perm in aperms:
		clients_group.permissions.add(perm)
	aperms = get_perms(maires, model)
	for perm in aperms:
		maires_group.permissions.add(perm)
	aperms = get_perms(services, model)
	for perm in aperms:
		services_group.permissions.add(perm)