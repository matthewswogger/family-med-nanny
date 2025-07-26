
class LogTemplate(str):
    DEFAULT_TEMPLATE = '{levelname} - {asctime} - {name} - {message}'
    FORMAT_TEMPLATE = '{levelname:<10}Timestamp: {asctime} : {name} : {message}'

    def __new__(cls, template=None):
        if template is None:
            template = cls.DEFAULT_TEMPLATE
        return super().__new__(cls, template)

    def __init__(self, template=None):
        self.template = template or self.DEFAULT_TEMPLATE
        super().__init__()

    def format(self, **kwargs):
        kwargs['asctime'] = kwargs['asctime'].replace(',', '.')
        kwargs['levelname'] = f"{kwargs['levelname']}:"

        return self.FORMAT_TEMPLATE.format(**kwargs)

    def __repr__(self):
        return f'{super().__repr__()}'


def async_cached(cache):
    """
    Async-compatible caching decorator that caches the result, not the coroutine.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Create a cache key based on function name only
            cache_key = func.__name__

            # Check if result is in cache
            if cache_key in cache:
                return cache[cache_key]

            # Execute the function and cache the result
            result = await func(*args, **kwargs)
            cache[cache_key] = result
            return result
        return wrapper
    return decorator
