"""This module includes all the Permissions
    that is needed to make authorized access to views.

"""

from rest_framework import permissions, status
from Sumino.redisDriver.utils import check_user_block_status
from rest_framework import exceptions
from Sumino.settings import SUM_REQUEST_LIMIT, WRONG_REQUEST_LIMIT


class UserIsBlockedPermission(permissions.BasePermission):
    """Permission check for users to see if he's been blocked
        due to sending too many "wrong" requests.
    """
    message = {"response": "You don't have the permission to call all the APIs till the next hour "
                           "due to too Many Wrong Requests in one hour! "}

    def has_permission(self, request, view):
        key = f"{request.META['REMOTE_ADDR']}_wrong"
        is_blocked = check_user_block_status(key, limit=WRONG_REQUEST_LIMIT)

        if is_blocked is True:  # The blocked user does not have the permission to request
            raise exceptions.Throttled(detail=self.message, code=status.HTTP_429_TOO_MANY_REQUESTS)
        return True


class UserIsSumBlockedPermission(permissions.BasePermission):
    """Permission check for users to see if he's been blocked
        due to sending too many requests to the "Sum" API.
    """
    message = {"response": "You don't have the permission to call all the Sum API till the next hour "
                           "due to too Many Requests in one hour! "}

    def has_permission(self, request, view):
        key = f"{request.META['REMOTE_ADDR']}_sum"
        is_blocked = check_user_block_status(key, limit=SUM_REQUEST_LIMIT)

        if is_blocked is True:  # The blocked user does not have the permission to request
            raise exceptions.Throttled(detail=self.message, code=status.HTTP_429_TOO_MANY_REQUESTS)
        return True
