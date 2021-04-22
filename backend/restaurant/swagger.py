from restaurant.models import PendingRestaurant, Restaurant, UserFavRestrs, PendingFood
from restaurant.enum import Prices, Payment

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import serializers
from rest_framework.response import Response

# Dish APIs sample requests and responses
dish_all_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "Dishes": [
                    {
                        "category": "Popular Dish",
                        "description": "kk",
                        "name": "new dish name",
                        "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                        "price": "10.00",
                        "restaurant_id": "605cbe3de8bf2b279ae052ed",
                        "specials": "",
                        "status": "Pending",
                        "_id": "605cee3ce8bf2b279ae052ef"
                    },
                    {
                        "category": "Special",
                        "description": "hhhhhh",
                        "name": "test dish",
                        "picture": "https://storage.googleapis.com/dev-scdining/FILE-uoffooxwgv-2021-03-29 13:43:36.357031.png",
                        "price": "10.00",
                        "restaurant_id": "60620fbc54201dbec7fd61b9",
                        "specials": "",
                        "status": "Pending",
                        "_id": "606211c754201dbec7fd61bb"
                    }
                ]
            }
        }
    )
}

dish_approved_rest_id_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "Dishes": [
                    {
                        "category": "Popular Dish",
                        "description": "kk",
                        "name": "new dish name",
                        "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                        "price": "10.00",
                        "restaurant_id": "605cbe3de8bf2b279ae052ed",
                        "specials": "",
                        "status": "Pending",
                        "_id": "605cee3ce8bf2b279ae052ef"
                    },
                    {
                        "category": "Special",
                        "description": "test",
                        "name": "A special dish",
                        "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                        "price": "100.00",
                        "restaurant_id": "605cbe3de8bf2b279ae052ed",
                        "specials": "",
                        "status": "Pending",
                        "_id": "605d0046fb767cc1fbc8ff1e"
                    }
                ]
            }
        }
    )
}

dish_pending_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "Dishes": [
                    {
                        "category": "Popular Dish",
                        "description": "kk",
                        "name": "new dish name",
                        "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                        "price": "10.00",
                        "restaurant_id": "605cbe3de8bf2b279ae052ed",
                        "specials": "",
                        "status": "Pending",
                        "_id": "605cee3ce8bf2b279ae052ef"
                    },
                    {
                        "category": "Special",
                        "description": "test",
                        "name": "A special dish",
                        "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                        "price": "100.00",
                        "restaurant_id": "605cbe3de8bf2b279ae052ed",
                        "specials": "",
                        "status": "Pending",
                        "_id": "605d0046fb767cc1fbc8ff1e"
                    }
                ]
            }
        }
    )
}


class PendingFoodInsertUpdate(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=100, decimal_places=2, min_value=0.00)
    specials = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        ref_name = None


dish_pending_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "category": "Popular Dish",
                "description": "kk",
                "name": "new dish name",
                "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                "price": "10.00",
                "restaurant_id": "605cbe3de8bf2b279ae052ed",
                "specials": "",
                "status": "Pending",
                "_id": "605cee3ce8bf2b279ae052ef"
            }
        }
    )
}

dish_pending_dish_id_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "category": "Popular Dish",
                "description": "updated kk",
                "name": "updated dish name",
                "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                "price": "100.00",
                "restaurant_id": "605cbe3de8bf2b279ae052ed",
                "specials": "",
                "status": "Pending",
                "_id": "605cee3ce8bf2b279ae052ef"
            }
        }
    )
}


dish_pending_dish_id_delete_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "category": "Popular Dish",
                "description": "deleted kk",
                "name": "deleted dish name",
                "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                "price": "100.00",
                "restaurant_id": "605cbe3de8bf2b279ae052ed",
                "specials": "",
                "status": "Pending",
                "_id": "605cee3ce8bf2b279ae052ef"
            }
        }
    )
}


class UserFavRest(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        ref_name = None


user_favourite_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "_id": "60722f7df1b220e1da21ee2c",
                "restaurant": {
                    "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                    "_id": "60633190ecd9bcd74ce3e50a",
                    "address": "1265 Military Trail",
                    "approved_once": True,
                    "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                    "categories": [],
                    "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                    "cuisines": [
                        "Greek"
                    ],
                    "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                    "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                    "email": "kbrahim-19970@filesy.site",
                    "facebook": "",
                    "full_menu_url": "",
                    "instagram": "",
                    "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                    "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                    "name": "Min's Restaurant",
                    "offer_options": "['Catering', 'Pick-up', 'Vegetarian Options', 'LLBO (Liquor License Board of Ontario)', 'Parking']",
                    "open_hours": "9-5",
                    "owner_first_name": [
                        "Min Qi"
                    ],
                    "owner_last_name": [
                        "Zhang"
                    ],
                    "owner_preferred_name": [
                        "Min"
                    ],
                    "owner_user_id": 8,
                    "payment_methods": "['Credit', 'Cash']",
                    "phone": 1231231234,
                    "postalCode": "M1C 1A4",
                    "pricepoint": "EXHIGH",
                    "restaurant_image_url": "[\"/\"]",
                    "restaurant_video_desc": "",
                    "restaurant_video_url": "/",
                    "status": "Approved",
                    "streetAddress2": "",
                    "streetAddress3": "",
                    "sysAdminComments": "",
                    "twitter": "",
                    "web_url": "",
                    "years": 4
                },
                "user_id": {
                    "auth_id": "",
                    "date_joined": "2021-03-22T18:18:14.051Z",
                    "email": "jenny100.yu@gmail.com",
                    "first_name": "Jenny",
                    "groups": [],
                    "id": 107,
                    "is_active": True,
                    "is_blocked": False,
                    "is_staff": False,
                    "is_superuser": False,
                    "last_login": "2021-04-05T14:38:12.605Z",
                    "last_name": "Yu",
                    "password": "pbkdf2_sha256$150000$89coNP8P8Vpy$dDgT1A59VaW8h+PvjxJveJjsDml9XNQbU5l2twT+7jY=",
                    "profile_id": 48,
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxODE4MjM4NywianRpIjoiOGVlYTczMjQwYjRmNDdiZTg0MGRlZWI0MjE0NzI3Y2YiLCJ1c2VyX2lkIjoxMDcsInJvbGUiOiJCVSIsInVzZXJuYW1lIjoiSmVubnkiLCJlbWFpbCI6Implbm55MTAwLnl1QGdtYWlsLmNvbSIsInByb2ZpbGVfaWQiOjQ4fQ.5FQitpJ0-apY1_KaPItyqwZbIjNPZy76tW4Ehtadt9w",
                    "role": "BU",
                    "user_permissions": [],
                    "username": "Jenny"
                }
            }
        }
    )
}

user_favourite_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": [
                {
                    "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                    "_id": "605b55d192c9e40e98c1877a",
                    "address": "431 Kwapis BLVD",
                    "approved_once": True,
                    "bio": "story",
                    "categories": [
                        "Popular Dish"
                    ],
                    "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                    "cuisines": [],
                    "deliveryDetails": "",
                    "dineinPickupDetails": "",
                    "email": "jenny100.yu@gmail.com",
                    "facebook": "",
                    "full_menu_url": "",
                    "instagram": "",
                    "locationNotes": "",
                    "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-qjebbwgdmo-2021-03-29 13:57:00.088590.png",
                    "name": "Jenny",
                    "offer_options": [
                        ""
                    ],
                    "open_hours": "9-5",
                    "owner_first_name": [
                        "k"
                    ],
                    "owner_last_name": [
                        "k"
                    ],
                    "owner_preferred_name": [],
                    "owner_user_id": 1,
                    "payment_methods": "['Credit', 'Debit', 'Cash']",
                    "phone": 1234567890,
                    "postalCode": "A1A 1A1",
                    "pricepoint": "MID",
                    "restaurant_image_url": "[\"https://storage.googleapis.com/dev-scdining/FILE-kiuawtkbba-2021-03-29 19:34:08.553788.png\", \"https://storage.googleapis.com/dev-scdining/FILE-ntwwpkpvtk-2021-03-29 19:34:09.507364.png\", \"https://storage.googleapis.com/dev-scdining/FILE-koeriryyrd-2021-03-29 19:34:10.012326.png\"]",
                    "restaurant_video_desc": "video description",
                    "restaurant_video_url": "https://www.youtube.com/watch?v=gzfzwAR7Atw",
                    "status": "Approved",
                    "streetAddress2": "",
                    "streetAddress3": "",
                    "sysAdminComments": "",
                    "twitter": "",
                    "web_url": "",
                    "years": 0
                }
            ]
        }
    )
}

restaurant_rest_id_favourited_users_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": [
                {
                    "auth_id": "",
                    "date_joined": "2021-03-22T18:18:14.051Z",
                    "email": "jenny100.yu@gmail.com",
                    "first_name": "Jenny",
                    "groups": [],
                    "id": 107,
                    "is_active": True,
                    "is_blocked": False,
                    "is_staff": False,
                    "is_superuser": False,
                    "last_login": "2021-04-05T14:38:12.605Z",
                    "last_name": "Yu",
                    "password": "pbkdf2_sha256$150000$89coNP8P8Vpy$dDgT1A59VaW8h+PvjxJveJjsDml9XNQbU5l2twT+7jY=",
                    "profile_id": 48,
                    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxODE4MjM4NywianRpIjoiOGVlYTczMjQwYjRmNDdiZTg0MGRlZWI0MjE0NzI3Y2YiLCJ1c2VyX2lkIjoxMDcsInJvbGUiOiJCVSIsInVzZXJuYW1lIjoiSmVubnkiLCJlbWFpbCI6Implbm55MTAwLnl1QGdtYWlsLmNvbSIsInByb2ZpbGVfaWQiOjQ4fQ.5FQitpJ0-apY1_KaPItyqwZbIjNPZy76tW4Ehtadt9w",
                    "role": "BU",
                    "user_permissions": [],
                    "username": "Jenny"
                }
            ]
        }
    )
}

user_favourited_rest_id_delete_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message": "Successfully removed restaurant from user's favourites"
            }
        }
    )
}

restaurant_approved_rest_id_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                "_id": "60633190ecd9bcd74ce3e50a",
                "address": "1265 Military Trail",
                "approved_once": True,
                "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                "categories": [],
                "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                "cuisines": [
                    "Greek"
                ],
                "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                "email": "kbrahim-19970@filesy.site",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                "name": "Min's Restaurant",
                "offer_options": "['Catering', 'Pick-up', 'Vegetarian Options', 'LLBO (Liquor License Board of Ontario)', 'Parking']",
                "open_hours": "9-5",
                "owner_first_name": [
                    "Min Qi"
                ],
                "owner_last_name": [
                    "Zhang"
                ],
                "owner_preferred_name": [
                    "Min"
                ],
                "owner_user_id": 8,
                "payment_methods": "['Credit', 'Cash']",
                "phone": 1231231234,
                "postalCode": "M1C 1A4",
                "pricepoint": "EXHIGH",
                "restaurant_image_url": "[\"/\"]",
                "restaurant_video_desc": "",
                "restaurant_video_url": "/",
                "status": "Approved",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "",
                "years": 4
            }
        }
    )
}

restaurant_pending_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                "_id": "605b55d192c9e40e98c1877a",
                "address": "431 Kwapis BLVD",
                "approved_once": True,
                "bio": "story",
                "categories": [
                    "Popular Dish"
                ],
                "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                "cuisines": [],
                "deliveryDetails": "",
                "dineinPickupDetails": "",
                "email": "jenny100.yu@gmail.com",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "",
                "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-qjebbwgdmo-2021-03-29 13:57:00.088590.png",
                "name": "Jenny",
                "offer_options": "['']",
                "open_hours": "9-5",
                "owner_first_name": [
                    "k"
                ],
                "owner_last_name": [
                    "k"
                ],
                "owner_preferred_name": [],
                "owner_user_id": 1,
                "payment_methods": "['Credit', 'Debit', 'Cash']",
                "phone": 1234567890,
                "postalCode": "A1A 1A1",
                "pricepoint": "MID",
                "restaurant_image_url": "[\"https://storage.googleapis.com/dev-scdining/FILE-kiuawtkbba-2021-03-29 19:34:08.553788.png\", \"https://storage.googleapis.com/dev-scdining/FILE-ntwwpkpvtk-2021-03-29 19:34:09.507364.png\", \"https://storage.googleapis.com/dev-scdining/FILE-koeriryyrd-2021-03-29 19:34:10.012326.png\"]",
                "restaurant_video_desc": "video description",
                "restaurant_video_url": "https://www.youtube.com/watch?v=gzfzwAR7Atw",
                "status": "Pending",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "",
                "years": 0
            }
        }
    )
}

restaurant_all_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "Restaurants": [
                    {
                        "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                        "_id": "605b55d192c9e40e98c1877a",
                        "address": "431 Kwapis BLVD",
                        "approved_once": True,
                        "bio": "story",
                        "categories": [
                            "Popular Dish"
                        ],
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "cuisines": [],
                        "deliveryDetails": "",
                        "dineinPickupDetails": "",
                        "email": "jenny100.yu@gmail.com",
                        "facebook": "",
                        "full_menu_url": "",
                        "instagram": "",
                        "locationNotes": "",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-qjebbwgdmo-2021-03-29 13:57:00.088590.png",
                        "name": "Jenny",
                        "offer_options": [
                            ""
                        ],
                        "open_hours": "9-5",
                        "owner_first_name": [
                            "k"
                        ],
                        "owner_last_name": [
                            "k"
                        ],
                        "owner_preferred_name": [],
                        "owner_user_id": 1,
                        "payment_methods": [
                            "Credit",
                            "Debit",
                            "Cash"
                        ],
                        "phone": 1234567890,
                        "postalCode": "A1A 1A1",
                        "pricepoint": "MID",
                        "restaurant_image_url": [
                            "https://storage.googleapis.com/dev-scdining/FILE-kiuawtkbba-2021-03-29 19:34:08.553788.png",
                            "https://storage.googleapis.com/dev-scdining/FILE-ntwwpkpvtk-2021-03-29 19:34:09.507364.png",
                            "https://storage.googleapis.com/dev-scdining/FILE-koeriryyrd-2021-03-29 19:34:10.012326.png"
                        ],
                        "restaurant_video_desc": "video description",
                        "restaurant_video_url": "https://www.youtube.com/watch?v=gzfzwAR7Atw",
                        "status": "Approved",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "sysAdminComments": "",
                        "twitter": "",
                        "web_url": "",
                        "years": 0
                    },
                    {
                        "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                        "_id": "60633190ecd9bcd74ce3e50a",
                        "address": "1265 Military Trail",
                        "approved_once": True,
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "categories": [],
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "cuisines": [
                            "Greek"
                        ],
                        "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "email": "kbrahim-19970@filesy.site",
                        "facebook": "",
                        "full_menu_url": "",
                        "instagram": "",
                        "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                        "name": "Min's Restaurant",
                        "offer_options": [
                            "Catering",
                            "Pick-up",
                            "Vegetarian Options",
                            "LLBO (Liquor License Board of Ontario)",
                            "Parking"
                        ],
                        "open_hours": "9-5",
                        "owner_first_name": [
                            "Min Qi"
                        ],
                        "owner_last_name": [
                            "Zhang"
                        ],
                        "owner_preferred_name": [
                            "Min"
                        ],
                        "owner_user_id": 8,
                        "payment_methods": [
                            "Credit",
                            "Cash"
                        ],
                        "phone": 1231231234,
                        "postalCode": "M1C 1A4",
                        "pricepoint": "EXHIGH",
                        "restaurant_image_url": [
                            "/"
                        ],
                        "restaurant_video_desc": "",
                        "restaurant_video_url": "/",
                        "status": "Approved",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "sysAdminComments": "",
                        "twitter": "",
                        "web_url": "",
                        "years": 4
                    },
                    {
                        "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                        "_id": "606c67d572a3c3069cf8621a",
                        "address": "1265 Military Trail",
                        "approved_once": True,
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "categories": [],
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "cuisines": [
                            "Greek"
                        ],
                        "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "email": "kbrahim-19971@filesy.site",
                        "facebook": "",
                        "full_menu_url": "",
                        "instagram": "",
                        "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                        "name": "A Restaurant",
                        "offer_options": [
                            "Catering",
                            "Pick-up",
                            "Vegetarian Options",
                            "LLBO (Liquor License Board of Ontario)",
                            "Parking"
                        ],
                        "open_hours": "9-5",
                        "owner_first_name": [
                            "Min Qi"
                        ],
                        "owner_last_name": [
                            "Zhang"
                        ],
                        "owner_preferred_name": [
                            "Min"
                        ],
                        "owner_user_id": 8,
                        "payment_methods": [
                            "Credit",
                            "Cash"
                        ],
                        "phone": 1231231234,
                        "postalCode": "M1C 1A4",
                        "pricepoint": "EXHIGH",
                        "restaurant_image_url": [
                            "/"
                        ],
                        "restaurant_video_desc": "",
                        "restaurant_video_url": "/",
                        "status": "Approved",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "sysAdminComments": "",
                        "twitter": "",
                        "web_url": "",
                        "years": 4
                    }
                ]
            }
        }
    )
}


class PendingRestaurantDraftInsertUpdate(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    years = serializers.CharField(required=False)
    address = serializers.CharField(max_length=60)
    streetAddress2 = serializers.CharField(required=False, max_length=50)
    streetAddress3 = serializers.CharField(required=False, max_length=50)
    postalCode = serializers.CharField(max_length=7)

    phone = serializers.IntegerField(required=False)
    email = serializers.EmailField()
    pricepoint = serializers.ChoiceField(
        required=False, choices=Prices.choices())
    cuisines = serializers.ListField(required=False)

    offer_options = serializers.ListField(required=False)

    owner_first_name = serializers.ListField()
    owner_last_name = serializers.ListField()
    owner_preferred_name = serializers.ListField(required=False)

    deliveryDetails = serializers.CharField(required=False, max_length=2000)
    dineinPickupDetails = serializers.CharField(
        required=False, max_length=2000)
    locationNotes = serializers.CharField(required=False, max_length=2000)

    bio = serializers.CharField(required=False)
    web_url = serializers.CharField(required=False, max_length=200)
    facebook = serializers.CharField(required=False, max_length=200)
    twitter = serializers.CharField(required=False, max_length=200)
    instagram = serializers.CharField(required=False, max_length=200)
    open_hours = serializers.CharField(required=False)
    payment_methods = serializers.ChoiceField(
        required=False, choices=Payment.choices())

    class Meta:
        ref_name = None


restaurant_draft_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                "_id": "605b55d192c9e40e98c1877a",
                "address": "431 Kwapis BLVD",
                "approved_once": False,
                "bio": "story",
                "categories": [],
                "cover_photo_url": "",
                "cuisines": [],
                "deliveryDetails": "",
                "dineinPickupDetails": "",
                "email": "jenny100.yu@gmail.com",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "",
                "logo_url": "",
                "name": "Jenny's Diner",
                "offer_options": "['']",
                "open_hours": "",
                "owner_first_name": ["Jenny"],
                "owner_last_name": ["Yu"],
                "owner_preferred_name": [],
                "owner_user_id": 1,
                "payment_methods": "['']",
                "phone": 1234567890,
                "postalCode": "A1A 1A1",
                "pricepoint": "",
                "restaurant_image_url": "['']",
                "restaurant_video_desc": "",
                "restaurant_video_url": "",
                "status": "Pending",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "",
                "years": 0
            }
        }
    )
}

restaurant_draft_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                "_id": "605b55d192c9e40e98c1877a",
                "address": "431 Kwapis BLVD",
                "approved_once": False,
                "bio": "Updated story",
                "categories": [],
                "cover_photo_url": "",
                "cuisines": ["Greek", "Vietnamese"],
                "deliveryDetails": "Some delivery details...",
                "dineinPickupDetails": "Some dine-in details...",
                "email": "jenny100.yu@gmail.com",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "Some location notes...",
                "logo_url": "",
                "name": "Jenny's Diner Updated",
                "offer_options": "['Pick-up', 'Delivery', 'Dine-in']",
                "open_hours": "9:00am-5:00pm Everyday",
                "owner_first_name": ["Jenny"],
                "owner_last_name": ["Yu"],
                "owner_preferred_name": [],
                "owner_user_id": 1,
                "payment_methods": "['']",
                "phone": 1234567890,
                "postalCode": "A1A 1A1",
                "pricepoint": "",
                "restaurant_image_url": "['']",
                "restaurant_video_desc": "",
                "restaurant_video_url": "",
                "status": "Pending",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "https://website.com",
                "years": 0
            }
        }
    )
}


class PendingRestaurantSubmit(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    years = serializers.CharField()
    address = serializers.CharField(max_length=60)
    streetAddress2 = serializers.CharField(required=False, max_length=50)
    streetAddress3 = serializers.CharField(required=False, max_length=50)
    postalCode = serializers.CharField(max_length=7)

    phone = serializers.IntegerField()
    email = serializers.EmailField()
    pricepoint = serializers.ChoiceField(choices=Prices.choices())
    cuisines = serializers.ListField(required=False)

    offer_options = serializers.ListField()

    owner_first_name = serializers.ListField()
    owner_last_name = serializers.ListField()
    owner_preferred_name = serializers.ListField(required=False)

    deliveryDetails = serializers.CharField(required=False, max_length=2000)
    dineinPickupDetails = serializers.CharField(
        required=False, max_length=2000)
    locationNotes = serializers.CharField(required=False, max_length=2000)

    bio = serializers.CharField()
    web_url = serializers.CharField(required=False, max_length=200)
    facebook = serializers.CharField(required=False, max_length=200)
    twitter = serializers.CharField(required=False, max_length=200)
    instagram = serializers.CharField(required=False, max_length=200)
    open_hours = serializers.CharField()
    payment_methods = serializers.ChoiceField(choices=Payment.choices())

    class Meta:
        ref_name = None


restaurant_submit_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                "_id": "605b55d192c9e40e98c1877a",
                "address": "431 Kwapis BLVD",
                "approved_once": False,
                "bio": "Restaurant's story",
                "categories": [],
                "cover_photo_url": "",
                "cuisines": [],
                "deliveryDetails": "",
                "dineinPickupDetails": "",
                "email": "jenny100.yu@gmail.com",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "",
                "logo_url": "",
                "name": "Jenny's Diner",
                "offer_options": "['Pick-up', 'Delivery', 'Dine-in']",
                "open_hours": "9:00am-5:00pm Everyday",
                "owner_first_name": ["Jenny"],
                "owner_last_name": ["Yu"],
                "owner_preferred_name": [],
                "owner_user_id": 1,
                "payment_methods": "['Credit', 'Debit', 'Cash']",
                "phone": 1234567890,
                "postalCode": "A1A 1A1",
                "pricepoint": "MID",
                "restaurant_image_url": "['']",
                "restaurant_video_desc": "",
                "restaurant_video_url": "",
                "status": "Pending",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "",
                "years": 0
            }
        }
    )
}


class RestaurantPostInsert(serializers.Serializer):
    restaurant_id = serializers.CharField()
    content = serializers.CharField(max_length=4096)

    class Meta:
        ref_name = None


restaurant_post_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "content": "New holiday sale at restaurant right now!",
                "owner_user_id": 0,
                "restaurant_id": "605b55d192c9e40e98c1877a",
                "timestamp": "2021-04-09T19:52:21.379+00:00",
                "_id": "6070b075e627f61867057dba"
            }
        }
    )
}

restaurant_post_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "Posts": [
                    {
                        "Timestamp": "Apr 09, 2021 19:52",
                        "_id": "6070b075e627f61867057dba",
                        "content": "Some restaurant post content",
                        "owner_user_id": 0,
                        "restaurant_id": "605b55d192c9e40e98c1877a"
                    }
                ]
            }
        }
    )
}

restaurant_post_post_id_delete_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "content": "Deleted restaurant post content",
                "owner_user_id": 0,
                "restaurant_id": "605b55d192c9e40e98c1877a",
                "timestamp": "2021-04-09T19:52:21.379+00:00",
                "_id": "6070b075e627f61867057dba"
            }
        }
    )
}

restaurant_media_put_request = [
    openapi.Parameter(
        'media_type', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, enum=["IMAGE", "VIDEO"]),
    openapi.Parameter(
        'save_location', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True,
        enum=["cover_photo_url", "logo_url", "restaurant_video_url", "restaurant_image_url"]),
    openapi.Parameter('media_file', in_=openapi.IN_FORM,
                      type=openapi.TYPE_FILE),
    openapi.Parameter('media_link', in_=openapi.IN_FORM,
                      type=openapi.TYPE_STRING),
    openapi.Parameter('submit_for_approval', in_=openapi.IN_FORM,
                      type=openapi.TYPE_STRING, required=True, enum=["True", "False"]),
]

restaurant_media_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                "_id": "605b55d192c9e40e98c1877a",
                "address": "431 Kwapis BLVD",
                "approved_once": True,
                "bio": "story",
                "categories": [
                    "Popular Dish"
                ],
                "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                "cuisines": [],
                "deliveryDetails": "",
                "dineinPickupDetails": "",
                "email": "jenny100.yu@gmail.com",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "",
                "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-qjebbwgdmo-2021-03-29 13:57:00.088590.png",
                "name": "Jenny",
                "offer_options": [
                    ""
                ],
                "open_hours": "9-5",
                "owner_first_name": [
                    "k"
                ],
                "owner_last_name": [
                    "k"
                ],
                "owner_preferred_name": [],
                "owner_user_id": 0,
                "payment_methods": [
                    "Credit",
                    "Debit",
                    "Cash"
                ],
                "phone": 1234567890,
                "postalCode": "A1A 1A1",
                "pricepoint": "MID",
                "restaurant_image_url": [
                    "https://storage.googleapis.com/dev-scdining/FILE-kiuawtkbba-2021-03-29 19:34:08.553788.png",
                    "https://storage.googleapis.com/dev-scdining/FILE-ntwwpkpvtk-2021-03-29 19:34:09.507364.png",
                    "https://storage.googleapis.com/dev-scdining/FILE-koeriryyrd-2021-03-29 19:34:10.012326.png"
                ],
                "restaurant_video_desc": "video description",
                "restaurant_video_url": "https://www.youtube.com/watch?v=gzfzwAR7Atw",
                "status": "Approved",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "",
                "years": 0
            }
        }
    )
}

restaurant_media_delete_request = [
    openapi.Parameter('restaurant_images', in_=openapi.IN_FORM,
                      type=openapi.TYPE_STRING, required=True)
]

restaurant_media_delete_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                "_id": "605b55d192c9e40e98c1877a",
                "address": "431 Kwapis BLVD",
                "approved_once": True,
                "bio": "story",
                "categories": [
                    "Popular Dish"
                ],
                "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                "cuisines": [],
                "deliveryDetails": "",
                "dineinPickupDetails": "",
                "email": "jenny100.yu@gmail.com",
                "facebook": "",
                "full_menu_url": "",
                "instagram": "",
                "locationNotes": "",
                "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-qjebbwgdmo-2021-03-29 13:57:00.088590.png",
                "name": "Jenny",
                "offer_options": [
                    ""
                ],
                "open_hours": "9-5",
                "owner_first_name": [
                    "k"
                ],
                "owner_last_name": [
                    "k"
                ],
                "owner_preferred_name": [],
                "owner_user_id": 0,
                "payment_methods": [
                    "Credit",
                    "Debit",
                    "Cash"
                ],
                "phone": 1234567890,
                "postalCode": "A1A 1A1",
                "pricepoint": "MID",
                "restaurant_image_url": [
                    "https://storage.googleapis.com/dev-scdining/FILE-kiuawtkbba-2021-03-29 19:34:08.553788.png"
                ],
                "restaurant_video_desc": "video description",
                "restaurant_video_url": "https://www.youtube.com/watch?v=gzfzwAR7Atw",
                "status": "Approved",
                "streetAddress2": "",
                "streetAddress3": "",
                "sysAdminComments": "",
                "twitter": "",
                "web_url": "",
                "years": 0
            }
        }
    )
}

dish_media_put_request = [
    openapi.Parameter(
        'media_type', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, enum=["IMAGE"]),
    openapi.Parameter(
        'save_location', in_=openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, enum=["picture"]),
    openapi.Parameter('media_file', in_=openapi.IN_FORM,
                      type=openapi.TYPE_FILE, required=True)
]

dish_media_put_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "category": "Popular Dish",
                "description": "kk",
                "name": "dish name",
                "picture": "https://storage.googleapis.com/default-assets/no-image.png",
                "price": "100.00",
                "restaurant_id": "605cbe3de8bf2b279ae052ed",
                "specials": "",
                "status": "Pending",
                "_id": "605cee3ce8bf2b279ae052ef"
            }
        }
    )
}
