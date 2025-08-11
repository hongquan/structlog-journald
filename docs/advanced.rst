Advanced usage
==============

One advantage of using *journald* is that, we can attach extra info to each log entry and filter by that info.
One example is in multi-tenant system, normally logs from many tenants mix together, making us difficult to debug
for a particular tenant. With *journald* we can attach tenant ID and filter logs by a tenant ID.

To do so:

- Use the ``extra_field_prefix`` parameter of :py:class:`~structlog_journald.JournaldProcessor`.
- Pass extra data to logger's ``.info()``, ``.debug()`` methods via the key which matches the value above.

For example, we have a SaaS system to control farms for many customers. We make a convention to attach farm codename to logs via ``f_farm``.
We then initialize ``JournaldProcessor`` with ``extra_field_prefix='f_'``.

.. literalinclude:: ../examples/extra-fields.py

When viewing logs with ``journalctl``, we can filter with ``F_FARM`` option:

.. code-block:: shell

	journalctl -u our-unit F_FARM=tomato

See it in action:

.. asciinema:: 732895
