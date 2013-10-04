import search.models
from django.db.models import Model
import inspect

#TODO: Support many2many relationships

def export(obj):
    params = []
    for field in obj._meta.fields:
        value = getattr(obj, field.name)
        if isinstance(value, Model):
            value = export(value)
        else:
            value = repr(value)
        params.append("%s=%s" % (field.name, value))
    return "%s.get_or_create(%s)" % (obj.__class__.__name__, ", ".join(params))

models = dict(inspect.getmembers(search.models, inspect.isclass)).values()
for model in models:
    if hasattr(model,'objects'):
        instances = model.objects.all()
        for instance in instances:
            print export(instance)
