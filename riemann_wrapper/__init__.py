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
                    global_tags=['python']):
    """Yield a riemann wrapper with default values for
    the bernhard client, host and prefix"""

    global_client = client
    global_host = host

    def wrap_riemann(metric,
                     client=global_client,
                     host=global_host,
                     tags=[]):

        tags = global_tags + tags

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

                    if client and send_exceptions:
                        if callable(send_exceptions):
                            if not send_exceptions(e):
                                raise
                        client.send({'host': hostname,
                                     'service': metric_name + "-exceptions",
                                     'description': str(e),
                                     'tags': tags + ['exception'],
                                     'attributes': {'prefix': prefix},
                                     'state': exception_state,
                                     'metric': 1})
                    raise

                duration = (time.time() - started) * 1000
                if client:
                    client.send({'host': hostname,
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
