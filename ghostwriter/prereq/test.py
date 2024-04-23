from ghostwriter.rolodex.models import Client
from ghostwriter.commandcenter.forms import ExtraFieldsField

extra_fields = ExtraFieldsField(Client._meta.label)

print(extra_fields)
