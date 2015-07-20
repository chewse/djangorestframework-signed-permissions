Quick Start
===========

Install
-------

This package is available on `PyPI`_.

Install from PyPI with ``pip``:

.. code-block:: bash

    $ pip install djangorestframework-signed-permissions

.. _pypi: https://pypi.python.org/pypi/djangorestframework-signed-permissions


Permission Signing
==================

This package leverages django's signing framework to store permission
information in a way that can be distributed in a url. Simply put, the function
``sign_filter_permissions`` expects to be passed a dictionary of a certain
format that it will attempt to sign as JSON and then returns that signed
string. The format of that dictionary is as follows:

.. code:: python

    {
      '<app_label>.<app_model>':[
        {
          'filters': {<dictionary that will be **kwargs expanded and passed to <app_model>.objects.filter},
          'actions': [<list of viewset method names to grant access to>]
        },
      ],
    }


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
