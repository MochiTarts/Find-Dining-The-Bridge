# Constants required for restaurant and food models

FOOD_PICTURE = 'https://storage.googleapis.com/default-assets/no-image.png'
RESTAURANT_COVER = 'https://storage.googleapis.com/default-assets/cover.jpg'
RESTAURANT_LOGO = 'https://storage.googleapis.com/default-assets/logo.jpg'
DISHES = 'dishes.csv'

dish_editable = ["name", "description", "picture",
                 "price", "specials", "category", "status"
                 ]

restaurant_editable = [
    "name",
    "years",
    "address",
    "streetAddress2",
    "streetAddress3",
    "postalCode",
    "phone",
    "updated_at",
    "cuisines",
    "pricepoint",
    "offer_options",
    "deliveryDetails",
    "locationNotes",
    "dineinPickupDetails",
    "web_url",
    "facebook",
    "twitter",
    "instagram",
    "bio",
    "cover_photo_url",
    "logo_url",
    "restaurant_video_url",
    "restaurant_image_url",
    "owner_first_name",
    "owner_last_name",
    "owner_preferred_name",
    "owner_story",
    "owner_picture_url",
    "status",
    "modified_time",
    "sysAdminComments",
    "open_hours",
    "payment_methods",
    "full_menu_url",
    "restaurant_video_desc",
    "phone_ext"]

allowed_image_types = (
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/gif')

allowed_video_types = ('video/mp4')