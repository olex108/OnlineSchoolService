from rest_framework import permissions


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="Модераторы").exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.owner
