IP-Address detection
====================

This package stores the remote IP of the visitor in the model,
and passes it to :doc:`Akismet <akismet>` for spam detection.
The IP Address is read from the ``REMOTE_ADDR`` meta field.
In case your site is behind a HTTP proxy (e.g. using Gunicorn or a load balancer),
this would make all comments appear to be posted from the load balancer IP.

The best and most secure way to fix this, is using WsgiUnproxy_ middleware in your ``wsgi.py``:

.. code-block:: python

    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    from wsgiunproxy import unproxy

    application = get_wsgi_application()
    application = unproxy(trusted_proxies=settings.TRUSTED_X_FORWARDED_FOR_IPS)(application)

In your ``settings.py``, you can define which hosts may pass the ``X-Forwarded-For``
header in the HTTP request. For example:

.. code-block:: python

    TRUSTED_X_FORWARDED_FOR_IPS = (
        '11.22.33.44',
        '192.168.0.1',
    )

.. warning::

    Please don't try to read ``HTTP_X_FORWARDED_FOR`` blindly with a fallback to ``HTTP_REMOTE_ADDR``.
    These headers could be provided by hackers, effectively circumventing your IP-address checks.
    Use WsgiUnproxy_ instead, which protects against maliciously injected headers.

Amazon Web Services Support
---------------------------

For AWS hosting, there is also `wsgi-aws-unproxy`_
which does the same for all CloudFront IP addresses.

IP-Subnet filtering
-------------------

Use the ``netaddr`` package to trust a full IP-block, e.g. for Kubernetes Ingress:

.. code-block:: python

    from django.core.wsgi import get_wsgi_application
    from netaddr import IPNetwork
    from wsgiunproxy import unproxy

    application = get_wsgi_application()
    application = unproxy(trusted_proxies=IPNetwork('10.0.0.0/8'))(application)

.. _Akismet: http://akismet.com
.. _WsgiUnproxy: https://pypi.python.org/pypi/WsgiUnproxy
.. _wsgi-aws-unproxy: https://github.com/LabD/wsgi-aws-unproxy
