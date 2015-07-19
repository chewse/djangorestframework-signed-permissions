# -*- coding: utf-8 -*-

from django.core import signing


def sign_filter_permissions(permissions):
    """
    Return a compressed, signed dump of the json blob.

    This function expects a json blob that is a dictionary containing model
    dotted names as keys. Those keys each have a value that is a list of
    dictionaries, each of which contains the keys 'filters' and 'actions':
    The key 'filters' key is a dict that is a filter to be applied to a
    django queryset. The key 'actions' is a list of DRF methods that can
    be called for this model's viewset.

    For example:
        {
            'accounts.Account':
                [
                    {
                        'filters': {
                            'email': 'marcel@chewse.com',
                            'organizations__name': 'Chewse'
                        },
                        'actions': ['create', 'partial_update']
                    }
                ]
        }
    """
    permissions = {key.lower(): value for key, value in permissions.iteritems()}
    return signing.dumps(permissions, compress=True)


def unsign_filters_and_actions(sign, dotted_model_name):
    """Return the list of filters and actions for dotted_model_name."""
    permissions = signing.loads(sign)
    return permissions.get(dotted_model_name, [])
