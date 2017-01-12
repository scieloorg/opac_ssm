OPAC SSM
========

Static Storage Management for OPAC website

.. image:: https://travis-ci.org/scieloorg/opac_ssm.svg?branch=master
    :target: https://travis-ci.org/scieloorg/opac_ssm

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

:License: BSD


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Deployment
----------

The following details how to deploy this application.


GRPC Server
-----------

Command to generate GRPC class:

.. code-block:: python

    python -m grpc_tools.protoc -I grpc_ssm --python_out=grpc_ssm --grpc_python_out=grpc_ssm grpc_ssm/opac.proto


