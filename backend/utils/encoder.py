from django.core.serializers.json import DjangoJSONEncoder
from bson import ObjectId
import json


class BSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return DjangoJSONEncoder.default(self, o)
