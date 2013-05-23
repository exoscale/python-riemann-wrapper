import time
import socket
import bernhard
from functools import wraps

def riemann_wrapper(client=bernhard.Client(),
                    prefix="",
                    host=None,
                    global_tags=['python']):
    """Yield a riemann wrapper with default values for
    the bernhard client, host and prefix"""

    def wrap_riemann(metric,
                     client=client,
                     host=host,
                     tags=[]):

        tags = global_tags + tags

        print("host: " + str(host))
        def riemann_decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):

                if host:
                    hostname = host
                else:
                    hostname = socket.gethostname()

                started = time.time()
                metric_name = prefix + metric

                try:
                    response = f(*args, **kwargs)
                except Exception as e:
                    client.send({'host': hostname,
                                 'service': metric_name + "-exceptions",
                                 'description': str(e),
                                 'tags': tags + ['exception'],
                                 'state': 'critical',
                                 'metric': 1})
                    raise

                duration = (time.time() - started) * 1000
                client.send({'host': hostname,
                             'service': metric_name + "-time",
                             'tags': tags + ['duration'],
                             'metric': duration})
                return response
            return decorated_function
        return riemann_decorator
    return wrap_riemann
    

# default riemann wrapper                
wrap_riemann = riemann_wrapper()
