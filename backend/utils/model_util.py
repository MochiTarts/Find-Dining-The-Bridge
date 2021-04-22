from django.forms import model_to_dict

from utils.encoder import BSONEncoder
from utils.geo_controller import geocode

import json

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


def model_to_json(model, extra_params={}):
    """
    utility function for handling converting models to json serializable dicts
    :params-model: model you are converting
    :params-extra_params: extra parameters you want to include in the returned dict
    :return: dictionary containing all fields in the model converted to json serializable form
    """

    model_dict = model_to_dict(model)
    for elem in extra_params:
        model_dict[elem] = extra_params[elem]

    return json.loads(json.dumps(model_dict, cls=BSONEncoder))


def edit_model(model, body, editable):
    """
    Edit model data
    :param model: model to be edited
    :param body: body of fields
    :param editable: list of editable fields
    :return: None
    """
    editable_fields = list(set(body) & set(editable))
    for editable_field in editable_fields:
        setattr(model, editable_field, body[editable_field])


def update_model_geo(model, address):
    model.GEO_location = geocode(address)
    return model


def models_to_json(iterable):
    """
    serialize iterable of models
    :param iterable: iterable of models
    :return: list of serialized models
    """
    models = []
    for model in iterable:
        models.append(model_to_json(model))
    return models


def model_refresh(model_class, query):
    """
    Refresh model from db (workaround fix to _id not showing up)
    :param model_class: Class object for model
    :param query: query for searching correct model
    :return: updated model
    """
    model = model_class.objects.get(**query)
    return model
