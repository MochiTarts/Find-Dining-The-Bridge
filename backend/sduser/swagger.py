from django.contrib.auth import get_user_model
from sduser.enum import Roles

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework import serializers

User = get_user_model()


class UserSignUp(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.CharField()


user_signup_post_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                'message': "verification email has been sent. Please activate your account before sign in. If you don't receive an email, please check your spam folder or contact us from your email address and we can verify it for you."
            }
        }
    )
}

user_nearby_get_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": [
                {
                    "restaurant": {
                        "_id": "607f3191e516285e70402bae",
                        "owner_user_id": 55,
                        "name": "Jenny's Diner",
                        "years": 10,
                        "address": "431 Kwapis BLVD",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "postalCode": "L3X 3H5",
                        "phone": 4166688966,
                        "email": "fanficwriteronthelake@gmail.com",
                        "pricepoint": "LOW",
                        "cuisines": [
                            "French"
                        ],
                        "offer_options": "['']",
                        "dineinPickupDetails": "Details...",
                        "deliveryDetails": "Details...",
                        "locationNotes": "Details...",
                        "web_url": "",
                        "facebook": "",
                        "twitter": "",
                        "instagram": "https://www.instagram.com/northernsmokes1/?hl=en",
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut vel pellentesque nulla, eu varius magna. Cras sagittis mollis imperdiet. Aliquam tincidunt enim ut lacus molestie, nec dapibus felis posuere. Vivamus et maximus ante. Donec vel efficitur velit. Suspendisse consectetur hendrerit dui eu varius. Suspendisse semper bibendum interdum. Donec et justo augue. Integer lacus tortor, suscipit quis pharetra ultricies, pharetra eget erat. Vivamus ullamcorper feugiat metus, ac efficitur enim viverra et. Cras vulputate ex vitae aliquam consectetur. Quisque aliquam tortor vitae lorem suscipit, nec laoreet mi consequat. Mauris gravida mauris a felis egestas, quis auctor est egestas. Etiam quis commodo mi. Aliquam sed vestibulum ipsum. Aliquam in lorem ut mauris sagittis egestas vel vel tortor.\n\nVivamus ut orci et ante consequat commodo. Mauris urna erat, venenatis eget commodo sodales, mattis nec elit. Donec consequat euismod velit vel suscipit. Curabitur nec libero consectetur, tempor libero ut, mollis velit. Integer metus libero, elementum quis blandit vestibulum, porttitor quis est. Nulla non ex quis lorem posuere egestas nec vitae lectus. Ut cursus commodo semper. Fusce sed facilisis quam, quis tristique massa. Quisque at mauris mollis, maximus massa ut, commodo lorem. Aliquam elementum sapien ipsum, a cursus justo aliquet a. Fusce ante magna, vulputate at libero eu, rhoncus aliquet justo. Mauris porta, sapien sit amet interdum molestie, ipsum nulla imperdiet ante, ut ullamcorper ligula mauris egestas odio. Proin vitae massa a turpis aliquet egestas id vel nulla.",
                        "GEO_location": "{'lat': 44.0639871, 'lng': -79.4941817}",
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "logo_url": "https://storage.googleapis.com/default-assets/logo.jpg",
                        "restaurant_video_url": "https://www.youtube.com/watch?v=PkJNGGrdqJU",
                        "restaurant_image_url": "[\"https://storage.googleapis.com/dev-scdining/FILE-rvjhzehiag-2021-04-21 20:06:20.833947.png\", \"https://storage.googleapis.com/dev-scdining/FILE-aedhzikfol-2021-04-21 20:06:22.082456.png\", \"https://storage.googleapis.com/dev-scdining/FILE-vzzlheefdh-2021-04-21 20:06:22.905728.png\", \"https://storage.googleapis.com/dev-scdining/FILE-dfobogskxk-2021-04-21 20:06:23.779180.png\", \"https://storage.googleapis.com/dev-scdining/FILE-lqvgiqhxem-2021-04-21 20:06:24.485766.png\", \"https://storage.googleapis.com/dev-scdining/FILE-jdltbgnekj-2021-04-21 20:06:25.513236.png\"]",
                        "owner_first_name": [
                            "Jenny"
                        ],
                        "owner_last_name": [
                            "Yu"
                        ],
                        "owner_preferred_name": [
                            ""
                        ],
                        "categories": [
                            "Special"
                        ],
                        "status": "Approved",
                        "sysAdminComments": "",
                        "open_hours": "9-5",
                        "payment_methods": "['Debit', 'Cash', 'Credit']",
                        "full_menu_url": "https://www.webtoons.com/en/favorite",
                        "approved_once": True,
                        "restaurant_video_desc": "",
                        "phone_ext": 0
                    },
                    "distance": 0.09441842712978067
                },
                {
                    "restaurant": {
                        "_id": "60633190ecd9bcd74ce3e50a",
                        "owner_user_id": 8,
                        "name": "Min's Restaurant",
                        "years": 4,
                        "address": "1265 Military Trail",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "postalCode": "M1C 1A4",
                        "phone": 1231231234,
                        "email": "kbrahim-19970@filesy.site",
                        "pricepoint": "EXHIGH",
                        "cuisines": [
                            "Greek"
                        ],
                        "offer_options": "['Catering', 'Pick-up', 'Vegetarian Options', 'LLBO (Liquor License Board of Ontario)', 'Parking']",
                        "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "web_url": "",
                        "facebook": "",
                        "twitter": "",
                        "instagram": "",
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis. ",
                        "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                        "restaurant_video_url": "/",
                        "restaurant_image_url": "[\"/\"]",
                        "owner_first_name": [
                            "Min Qi"
                        ],
                        "owner_last_name": [
                            "Zhang"
                        ],
                        "owner_preferred_name": [
                            "Min"
                        ],
                        "categories": [],
                        "status": "Approved",
                        "sysAdminComments": "",
                        "open_hours": "9-5",
                        "payment_methods": "['Credit', 'Cash']",
                        "full_menu_url": "",
                        "approved_once": True,
                        "restaurant_video_desc": "",
                        "phone_ext": None
                    },
                    "distance": 39.827594937396
                },
                {
                    "restaurant": {
                        "_id": "606c67d572a3c3069cf8621a",
                        "owner_user_id": 8,
                        "name": "A Restaurant",
                        "years": 4,
                        "address": "1265 Military Trail",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "postalCode": "M1C 1A4",
                        "phone": 1231231234,
                        "email": "kbrahim-19971@filesy.site",
                        "pricepoint": "EXHIGH",
                        "cuisines": [
                            "Greek"
                        ],
                        "offer_options": "['Catering']",
                        "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "web_url": "",
                        "facebook": "",
                        "twitter": "",
                        "instagram": "",
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                        "restaurant_video_url": "/",
                        "restaurant_image_url": "[\"/\"]",
                        "owner_first_name": [
                            "Min Qi"
                        ],
                        "owner_last_name": [
                            "Zhang"
                        ],
                        "owner_preferred_name": [
                            "Min"
                        ],
                        "categories": [],
                        "status": "Approved",
                        "sysAdminComments": "",
                        "open_hours": "9-5",
                        "payment_methods": "['Credit', 'Cash']",
                        "full_menu_url": "",
                        "approved_once": True,
                        "restaurant_video_desc": "",
                        "phone_ext": None
                    },
                    "distance": 39.827594937396
                },
                {
                    "restaurant": {
                        "_id": "606c682572a3c3069cf8621b",
                        "owner_user_id": 8,
                        "name": "B Restaurant",
                        "years": 4,
                        "address": "1265 Military Trail",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "postalCode": "M1C 1A4",
                        "phone": 1231231234,
                        "email": "kbrahim-19972@filesy.site",
                        "pricepoint": "EXHIGH",
                        "cuisines": [
                            "Greek"
                        ],
                        "offer_options": "['Vegetarian Options', 'LLBO (Liquor License Board of Ontario)', 'Parking']",
                        "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "web_url": "",
                        "facebook": "",
                        "twitter": "",
                        "instagram": "",
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                        "restaurant_video_url": "/",
                        "restaurant_image_url": "[\"/\"]",
                        "owner_first_name": [
                            "Min Qi"
                        ],
                        "owner_last_name": [
                            "Zhang"
                        ],
                        "owner_preferred_name": [
                            "Min"
                        ],
                        "categories": [],
                        "status": "Approved",
                        "sysAdminComments": "",
                        "open_hours": "9-5",
                        "payment_methods": "['Credit', 'Cash']",
                        "full_menu_url": "",
                        "approved_once": True,
                        "restaurant_video_desc": "",
                        "phone_ext": None
                    },
                    "distance": 39.827594937396
                },
                {
                    "restaurant": {
                        "_id": "606c683c72a3c3069cf8621c",
                        "owner_user_id": 8,
                        "name": "C Restaurant",
                        "years": 4,
                        "address": "1265 Military Trail",
                        "streetAddress2": "",
                        "streetAddress3": "",
                        "postalCode": "M1C 1A4",
                        "phone": 1231231234,
                        "email": "kbrahim-19973@filesy.site",
                        "pricepoint": "EXHIGH",
                        "cuisines": [
                            "Greek"
                        ],
                        "offer_options": "['Pick-up', 'Vegetarian Options', 'Parking']",
                        "dineinPickupDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "deliveryDetails": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "locationNotes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "web_url": "",
                        "facebook": "",
                        "twitter": "",
                        "instagram": "",
                        "bio": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In nec mauris dictum, tempus mauris ac, tempor mi. Nullam laoreet rutrum nulla a dapibus. Praesent quis aliquam leo. Etiam turpis magna, semper ac mi sed, efficitur dignissim massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Curabitur placerat neque libero, non egestas nisl malesuada eget. Nullam sagittis tellus et diam luctus iaculis.",
                        "GEO_location": "{'lat': 43.7825084, 'lng': -79.1853174}",
                        "cover_photo_url": "https://storage.googleapis.com/default-assets/cover.jpg",
                        "logo_url": "https://storage.googleapis.com/dev-scdining/FILE-sdqptfczxm-2021-03-30 10:11:32.003390.png",
                        "restaurant_video_url": "/",
                        "restaurant_image_url": "[\"/\"]",
                        "owner_first_name": [
                            "Min Qi"
                        ],
                        "owner_last_name": [
                            "Zhang"
                        ],
                        "owner_preferred_name": [
                            "Min"
                        ],
                        "categories": [],
                        "status": "Approved",
                        "sysAdminComments": "",
                        "open_hours": "9-5",
                        "payment_methods": "['Credit', 'Cash']",
                        "full_menu_url": "",
                        "approved_once": True,
                        "restaurant_video_desc": "",
                        "phone_ext": None
                    },
                    "distance": 39.827594937396
                }
            ]
        }
    )
}
