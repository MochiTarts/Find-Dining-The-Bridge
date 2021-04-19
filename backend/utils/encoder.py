import json
from bson import ObjectId
from django.core.serializers.json import DjangoJSONEncoder


class BSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return DjangoJSONEncoder.default(self, o)
