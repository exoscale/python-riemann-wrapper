riemann_wrapper: time functions with riemann
============================================

Introductory blog post: http://www.spootnik.org/entries/2013/05/21_using-riemann-to-monitor-python-apps.html

This library is provided to allow timing and exception reporting
of python functions using http://riemann.io.

Installing
----------
Pip::

    pip install riemann_wrapper

Pypi: https://pypi.python.org/pypi/riemann_wrapper

Manual::

    python setup.py install

Usage
-----


Provide a metric name and a bernhard client for timing::

    import bernhard
    from riemann_wrapper import wrap_riemann, riemann_wrapper

    riemann = bernhard.Client()

    @wrap_riemann("cpu-intensive-task", client=riemann)
    def do_something_cpu_intensive():
       # [...]

Call options:
-------------

The following keyword args may be passed to ``wrap_riemann``:

* ``client``: instance of ``bernhard.Client`` to send events with
* ``tags``: tags to attach to riemann events
* ``host``: override hostname for the event
* ``logger``: a standard python logger to which transport errors may be logged

Alternately, a new wrapping function can be created by calling
``riemann_wrapper`` like-so::

    import bernhard
    from riemann_wrapper import wrap_riemann, riemann_wrapper

    riemann = bernhard.Client()
    my_wrapper = riemann_wrapper(client=bernhard.Client(), prefix="myapp.")

    @my_wrapper("cpu-intensive-task")
    def do_something_cpu_intensive():
       # [...]

The following keyword args may be passed to ``riemann_wrapper``:

* ``client``: instance of ``bernhard.Client`` to send events with
* ``global_tags``: tags present in all sent events. Default: ``['python']``.
* ``host``: override hostname for all events. Default: ``None``.
* ``logger``: a standard python logger to which transport errors may be logged.
  Default: ``None``.
* ``prefix``: prepend given string to all event services. Default: ``python``.
* ``exception_state``: state sent for exceptions. Default: ``'warning'``.
* ``send_exceptions``: boolean or callable that takes an exceptions as a
  parameter and returns a boolean to specify whether to send that particular
  exception to riemann. Default: True.
