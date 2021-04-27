# jsonschema validation schemas for restaurant and dish request bodies
food_insert_edit_schema = {
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "picture": {"type": "string"},
        "price": {"type": ["string", "number"]},
        "specials": {"type": "string"},
        "category": {"type": "string"}
    },
    "required": ["name", "description", "price", "specials", "category"],
    "additionalProperties": False
}

restaurant_insert_for_approval_schema = {
    "properties": {
        "name": {"type": "string"},
        "years": {"type": "number"},
        "address": {"type": "string"},
        "streetAddress2": {"type": "string"},
        "streetAddress3": {"type": "string"},
        "postalCode": {"type": "string"},

        "phone": {"type": "number"},
        "email": {"type": "string"},
        "cuisines": {"type": "array"},
        "pricepoint": {"type": "string"},

        "offer_options": {"type": "array"},

        "dineinPickupDetails": {"type": "string"},
        "deliveryDetails": {"type": "string"},
        "locationNotes": {"type": "string"},

        "web_url": {"type": "string"},
        "facebook": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "GEO_location": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"},
        "restaurant_video_desc": {"type": "string"},
        "phone_ext": {"type": "number"}
    },
    "required": ["name", "years", "address", "postalCode", "phone", "email", "pricepoint", "offer_options",
                 "bio", "owner_first_name", "owner_last_name", "open_hours", "payment_methods"],
    "additionalProperties": False
}

restaurant_insert_draft_schema = {
    "properties": {
        "name": {"type": "string"},
        "years": {"type": "number"},
        "address": {"type": "string"},
        "streetAddress2": {"type": "string"},
        "streetAddress3": {"type": "string"},
        "postalCode": {"type": "string"},

        "phone": {"type": "number"},
        "email": {"type": "string"},
        "cuisines": {"type": "array"},
        "pricepoint": {"type": "string"},

        "offer_options": {"type": "array"},

        "dineinPickupDetails": {"type": "string"},
        "deliveryDetails": {"type": "string"},
        "locationNotes": {"type": "string"},

        "web_url": {"type": "string"},
        "facebook": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"},
        "restaurant_video_desc": {"type": "string"},
        "phone_ext": {"type": "number"}
    },
    "required": ["name", "address", "postalCode", "email", "owner_first_name", "owner_last_name"],
    "additionalProperties": False
}

restaurant_edit_draft_schema = {
    "properties": {
        "name": {"type": "string"},
        "years": {"type": "number"},
        "address": {"type": "string"},
        "streetAddress2": {"type": "string"},
        "streetAddress3": {"type": "string"},
        "postalCode": {"type": "string"},

        "phone": {"type": "number"},
        "email": {"type": "string"},
        "cuisines": {"type": "array"},
        "pricepoint": {"type": "string"},

        "offer_options": {"type": "array"},

        "dineinPickupDetails": {"type": "string"},
        "deliveryDetails": {"type": "string"},
        "locationNotes": {"type": "string"},

        "web_url": {"type": "string"},
        "facebook": {"type": "string"},
        "twitter": {"type": "string"},
        "instagram": {"type": "string"},
        "bio": {"type": "string"},
        "cover_photo_url": {"type": "string"},
        "logo_url": {"type": "string"},
        "restaurant_video_url": {"type": "string"},
        "restaurant_image_url": {"type": "string"},

        "owner_first_name": {"type": "array"},
        "owner_last_name": {"type": "array"},
        "owner_preferred_name": {"type": "array"},

        "sysAdminComments": {"type": "string"},
        "categories": {"type": "array"},
        "status": {"type": "string"},

        "open_hours": {"type": "string"},
        "payment_methods": {"type": "array"},

        "full_menu_url": {"type": "string"},
        "restaurant_video_desc": {"type": "string"},
        "phone_ext": {"type": "number"}
    },
    "required": ["name", "address", "postalCode", "owner_first_name", "owner_last_name"],
    "additionalProperties": False
}

user_fav_schema = {
    "properties": {
        "restaurant": {"type": "string"}
    },
    "required": ["restaurant"],
    "additionalProperties": False
}

post_schema = {
    'properties': {
        'restaurant_id': {'type': 'string'},
        'content': {'type': 'string'}
    }
}