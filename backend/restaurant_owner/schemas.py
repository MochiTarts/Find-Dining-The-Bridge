# jsonschema validation schemas for request bodies
restaurant_owner_signup_schema = {
    "properties": {
        "restaurant_id": {"type": "string"},
        "consent_status": {"type": "string"},
    },
    "required": ["restaurant_id"],
    "additionalProperties": False
}

restaurant_owner_edit_schema = {
    "properties": {
        "consent_status": {"type": "string"},
    },
    "additionalProperties": False
}