from bson import ObjectId

def isObjectId(oid):
    return ObjectId.is_valid(oid)

def save_and_clean(model, updated_fields=None):
    """
    clean model and then save
    :params-model: referenced model
    :return: saved model
    """
    model.clean_fields()
    model.clean()
    if updated_fields:
        model.save(update_fields=updated_fields)
    else:
        model.save()
    return model