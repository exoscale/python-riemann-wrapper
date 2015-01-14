import time
import socket
import bernhard
from functools import wraps


def riemann_wrapper(client=bernhard.Client(),
                    prefix="python",
                    sep=".",
                    host=None,
                    exception_state='warning',
                    send_exceptions=True,
                    global_tags=['python'],
                    logger=None):
    """Yield a riemann wrapper with default values for
    the bernhard client, host and prefix"""

    global_client = client
    global_host = host
    global_logger = logger

    def wrap_riemann(metric,
                     client=global_client,
                     host=global_host,
                     tags=[],
                     logger=global_logger):

        tags = global_tags + tags

        def send(event):
            if client:
                try:
                    client.send(event)
                except bernhard.TransportError:
                    log = _call_if_callable(logger)
                    if log:
                        log.exception('Failed to send Riemann event.')

        def riemann_decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):

                if host:
                    hostname = host
                else:
                    hostname = socket.gethostname()

                started = time.time()
                metric_name = prefix + sep + metric

                try:
                    response = f(*args, **kwargs)
                except Exception as e:

                    if _call_if_callable(send_exceptions, e):
                        send({'host': hostname,
                              'service': metric_name + "-exceptions",
                              'description': str(e),
                              'tags': tags + ['exception'],
                              'attributes': {'prefix': prefix},
                              'state': exception_state,
                              'metric': 1})
                    raise

                duration = (time.time() - started) * 1000
                send({'host': hostname,
                      'service': metric_name + "-time",
                      'attributes': {'prefix': prefix},
                      'tags': tags + ['duration'],
                      'metric': duration})
                return response
            return decorated_function
        return riemann_decorator
    return wrap_riemann


# default riemann wrapper
wrap_riemann = riemann_wrapper()


def _call_if_callable(x, *args):
    return x(*args) if callable(x) else x
