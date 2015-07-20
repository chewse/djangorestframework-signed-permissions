# -*- coding: utf-8 -*-

from django.core import signing
from django.core.exceptions import FieldError

from .signing import unsign_filters_and_actions


class SignedViewSetMixin(object):
    """
    Mixin that is added to a ViewSet to properly filter its queryset.

    This calls the same mechanisms that are used to determine permissioning.
    """

    def get_queryset(self):
        """Return the allowed queryset for this sign or the default one."""
        if 'sign' in self.request.query_params:
            try:
                filter_and_actions = unsign_filters_and_actions(
                    self.request.query_params['sign'],
                    '{}.{}'.format(
                        self.queryset.model.app_label,
                        self.queryset.model.model_name,
                    )
                )
            except signing.BadSignature:
                return super(SignViewSetMixin, self).get_queryset()
            else:
                for filtered_action in filter_and_actions:
                    try:
                        qs = self.queryset.filter(**filtered_action['filters'])
                    except FieldError:
                        continue
                    return qs
        return super(SignViewSetMixin, self).get_queryset()
