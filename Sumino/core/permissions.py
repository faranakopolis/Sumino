"""This module includes all the Permissions
    that is needed to make authorized access to views.

"""

from rest_framework import permissions
from Sumino.redisDriver.utils import check_user_block_status
from rest_framework import exceptions


class UserIsBlockedPermission(permissions.BasePermission):
    """Permission check for users to see if he's been blocked
        because of sending too many wrong requests.
    """
    message = {"response": "You don't have the permission to call all the APIs till the next hour "
                           "due to too Many Wrong Requests in one hour! "}

    def has_permission(self, request, view):
        is_blocked = check_user_block_status(request.META['REMOTE_ADDR'])

        # a blocked user (is_blocked=True) shouldn't have the permission => False
        has_permission_to_request = not is_blocked

        if has_permission_to_request is False:
            raise exceptions.PermissionDenied(detail=self.message)
        else:
            return True
