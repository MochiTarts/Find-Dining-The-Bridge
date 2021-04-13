from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

article_all_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "articles": [
                    {
                        "author": "Bob",
                        "content": "<p>Article content</p>",
                        "created_at": "2021-04-05T17:56:05.827000Z",
                        "id": 1,
                        "links": "https://www.google.com/, https://www.google.ca",
                        "modified_at": "2021-04-05T17:56:05.827000Z",
                        "published": True,
                        "thumbnail": "Screen_Shot_2021-04-04_at_9.18.35_PM.png",
                        "title": "General Public Title",
                        "visibility": "ALL"
                    },
                    {
                        "author": "Mary",
                        "content": "<p>Article content 2</p>",
                        "created_at": "2021-05-05T17:56:05.827000Z",
                        "id": 2,
                        "links": "https://www.yahoo.com/, https://www.facebook.com",
                        "modified_at": "2021-05-05T17:56:05.827000Z",
                        "published": True,
                        "thumbnail": "Screen_Shot_2021-04-04_at_9.18.35_PM.png",
                        "title": "Article Title for Public",
                        "visibility": "ALL"
                    }
                ],
            }
        }
    )
}

article_id_response = {
    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "articles": [
                    {
                        "author": "Gabe",
                        "content": "<p>Article content</p>",
                        "created_at": "2021-04-05T17:56:05.827000Z",
                        "id": 1,
                        "links": "https://www.google.com/, https://www.google.ca",
                        "modified_at": "2021-04-05T17:56:05.827000Z",
                        "published": True,
                        "thumbnail": "Screen_Shot_2021-04-04_at_9.18.35_PM.png",
                        "title": "BU only Title",
                        "visibility": "BU"
                    }
                ],
            }
        }
    )
}
