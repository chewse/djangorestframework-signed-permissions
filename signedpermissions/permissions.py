# -*- coding: utf-8 -*-

from django.core import signing
from rest_framework import permissions

from .signing import unsign_filters_and_actions


class SignedPermission(permissions.BasePermission):
    """
    Allow access to a particular set of filters if the sign is valid.

    This permission allows access to sets of items based on json encoded
    filters. It takes these filters and applies to them to the proper queryset
    use **kwargs expansion, or in the case of a create (POST), it checks the
    POST data.
    """

    def has_permission(self, request, view):
        """Check list and create permissions based on sign and filters."""
        if view.suffix == 'Instance':
            return True

        filter_and_actions = self._get_filter_and_actions(
            request.query_params.get('sign'),
            view.action,
            '{}.{}'.format(
                view.queryset.model._meta.app_label,
                view.queryset.model._meta.model_name
            )
        )
        if not filter_and_actions:
            return False
        if request.method == 'POST':
            for key, value in request.data.iteritems():
                # Do unicode conversion because value will always be a
                # string
                if (key in filter_and_actions['filters'] and not
                        unicode(filter_and_actions['filters'][key]) == value):
                    return False
        return True

    def has_object_permission(self, request, view, obj=None):
        """Check object permissions based on filters."""
        filter_and_actions = self._get_filter_and_actions(
            request.query_params.get('sign'),
            view.action,
            '{}.{}'.format(obj._meta.app_label, obj._meta.model_name))
        if not filter_and_actions:
            return False
        qs = view.queryset.filter(**filter_and_actions['filters'])
        return qs.filter(id=obj.id).exists()

    @staticmethod
    def _get_filter_and_actions(sign, action, dotted_model_name):
        try:
            filters_and_actions = unsign_filters_and_actions(
                sign,
                dotted_model_name
            )
        except signing.BadSignature:
            return {}
        for filtered_action in filters_and_actions:
            if action in filtered_action['actions']:
                return filtered_action
        return {}
