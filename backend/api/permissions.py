from rest_framework import permissions


class IsOwnerCitizen(permissions.BasePermission):
	"""
	for only Citizen owner, model should has citizen attribut
	"""
	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated()

	def has_object_permission(self, request, view, obj):
		return obj.citizen == request.user

class IsOwnerMaire(permissions.BasePermission):
	"""
	for only Maire owner, model should has maire attribut
	"""
	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated()

	def has_object_permission(self, request, view, obj):
		return obj.maire == request.user

class IsOwnerService(permissions.BasePermission):
	"""
	for only Service owner, model should has service attribut
	"""
	def has_permission(self, request, view):
		return request.user and request.user.is_authenticated()

	def has_object_permission(self, request, view, obj):
		return obj.service == request.user