# jsonschema validation scheme
newsletter_signup_schema = {
    "properties": {
        "first_name": {
            "type": "string",
            "minLength": 1,
            "error_msg": "First name cannot be empty."
        },
        "last_name": {
            "type": "string",
            "minLength": 1,
            "error_msg": "Last name cannot be empty."
        },
        "email": {
            "type": "string",
            "minLength": 1,
            "error_msg": "Email cannot be empty."
        },
        "consent_status": {
            "type": "string",
            "minLength": 1,
            "error_msg": "Consent status cannot be empty."
        }
    },
    "required": ["first_name", "last_name", "email", "consent_status"]
}