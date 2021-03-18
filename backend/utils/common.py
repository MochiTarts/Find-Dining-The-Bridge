from bson import ObjectId

def isObjectId(oid):
    return ObjectId.is_valid(oid)