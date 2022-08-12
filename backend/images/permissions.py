from rest_framework import permissions


class DownloadLinkAllowed(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.account_perm and request.account_perm.allow_download)