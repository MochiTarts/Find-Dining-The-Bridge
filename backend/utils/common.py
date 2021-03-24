from bson import ObjectId
from sduser.backends import jwt_decode

def isObjectId(oid):
    return ObjectId.is_valid(oid)

def save_and_clean(model, updated_fields=None):
    """
    clean model and then save
    :params-model: referenced model
    :return: saved model
    """
    try:
        model.clean_fields()
        model.clean()
        if updated_fields:
            model.save(update_fields=updated_fields)
        else:
            model.save()
        return model
    except Exception as err:
        print(err)
        raise err

def get_user(header):
    if header.startswith('Bearer'):
        token = header.split(' ')[1]
        return jwt_decode(token)
    else:
        return False