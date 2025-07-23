
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
