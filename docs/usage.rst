Quick Start
===========

Install
-------

This package is available on `PyPI`_.

Install from PyPI with ``pip``:

.. code-block:: bash

    $ pip install djangorestframework-signed-permissions

.. _pypi: https://pypi.python.org/pypi/djangorestframework-signed-permissions


Example
=======


MyViews.py
----------

.. code:: python

    from rest_framework import viewsets
    from signedpermissions import SignedPermission, SignedViewSetMixin


    class MyViewSet(SignedViewSetMixin, viewsets.ModelViewSet):
       ...
       permission_classes = [SignedPermission,]


Models.py
---------

.. code:: python

    from django.db import models

    class MyModel(models.Model):
      ...
      owner = models.ForeignKey('owners.Owner')


Emailer.py
----------

.. code:: python

    from signedpermissions import sign_filter_permissions


    def send_email(owner_id):
      ...
      object_permissions = {
        'myapp.MyModel': [
          {
            'filters': {
              'owner_id': owner_id
            },
            'actions': ['create', 'retrieve', 'update', 'partial_update',],
          }
        ]
      }
      BASE_URL = 'http://example.com'
      signature = sign_filter_permissions(object_permissions)
      url = '{}?sign={}'.format(BASE_URL, signature)

      # Send email with url
      ...
