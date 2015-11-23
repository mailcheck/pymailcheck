pymailcheck
===========

Suggest corrections to user-misspelled email addresses.

Python port of `mailcheck.js <https://github.com/mailcheck/mailcheck/>`_.

Installation
------------

.. code-block:: bash

    $ python setup.py install

Usage
-----

.. code-block:: python

    >>> import pymailcheck
    >>> pymailcheck.suggest("test@example.con")
    {'domain': 'example.com', 'full': 'test@example.com', 'address': 'test'}
    >>> pymailcheck.suggest("test@example.org")
    False

You can override or append the built-in list of domains, top-level domains,
and/or second-level domains:

=====================  ================================ =========
Parameter              Defaults                         Example
=====================  ================================ =========
domains                pymailcheck.DOMAINS              yahoo.com
top_level_domains      pymailcheck.TOP_LEVEL_DOMAINS    yahoo
second_level_domains   pymailcheck.SECOND_LEVEL_DOMAINS com
=====================  ================================ =========

.. code-block:: python

    >>> pymailcheck.suggest("test@contosl.com")
    False
    >>> custom_domains = ["example.com", "contoso.com"]
    >>> pymailcheck.suggest("test@contosl.com", domains=custom_domains)
    {'domain': 'contoso.com', 'full': 'test@contoso.com', 'address': 'test'}

.. code-block:: python

    >>> pymailcheck.suggest("test@contosl.com")
    False
    >>> custom_domains = pymailcheck.DOMAINS.union(("example.com", "contoso.com"))
    >>> pymailcheck.suggest("test@contosl.com", domains=custom_domains)
    {'domain': 'contoso.com', 'full': 'test@contoso.com', 'address': 'test'}

Running Tests
-------------

.. code-block:: bash

    $ python -m unittest discover
