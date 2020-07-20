from functools import wraps
from inspect import signature


class ServiceProvider:

    def __init__(self):
        self._services = {}

    def register(self, name=None):

        def decorator(service):

            if name is None and not hasattr(service, "__name__"):
                raise ValueError
            service_name = name or service.__name__
            if not service_name:
                raise ValueError
            self._services[service_name] = service
            return service

        return decorator

    def inject(self, *s, **kws):

        def decorator(func):

            @wraps(func)
            def decorated(*args, **kwargs):
                new_args = ()
                arg_index = 0
                for name, param in signature(func).parameters.items():
                    if name in self._services and name in s:
                        arg = self._services[name]
                    elif name in kws and kws[name] in self._services:
                        arg = self._services[kws[name]]
                    elif arg_index < len(args):
                        arg = args[arg_index]
                        arg_index += 1
                    elif name in kwargs or param.default != param.empty:
                        continue
                    else:
                        raise ValueError
                    new_args += (arg,)

                return func(*new_args, **kwargs)

            return decorated

        return decorator
