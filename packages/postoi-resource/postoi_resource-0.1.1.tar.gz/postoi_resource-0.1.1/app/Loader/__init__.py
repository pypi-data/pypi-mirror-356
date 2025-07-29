from .Loader        import Loader


def alter_schema(schema):
    from . import Models
    for s in schema:
        c = getattr(Models, s['class'])
        if hasattr(c, s['key']):
            setattr(c, s['key'], s['value'])

