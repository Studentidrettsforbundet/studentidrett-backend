from django.http import HttpResponse

from elasticsearch_dsl import Q, Search
from rest_framework.utils import json


def global_search(request):
    q = request.GET.get("q")

    q_list = q.split("/")  # If query is clubs/ntnui

    if len(q_list) != 1:
        response_list = specified_search(q_list[0], q_list[1])

    else:
        response_list = []
        if q:
            search = Search(index=["clubs", "cities", "groups", "sports"])
            query = Q(
                {
                    "multi_match": {
                        "query": q,
                        "fields": ["name", "description"],
                        "fuzziness": "AUTO",
                    }
                }
            )
            objects = search.query(query)
            response_list = []

            for item in objects:
                response_list.append(map_response_item(item))

    return HttpResponse(
        json.dumps(response_list), status=200, content_type="application/json"
    )


def specified_search(index, q):
    indices = ("clubs", "cities", "groups", "sports")
    response_list = []

    if index in indices:
        search = Search(index=[index])
        query = Q(
            {
                "multi_match": {
                    "query": q,
                    "fields": ["name", "description"],
                    "fuzziness": "AUTO",
                }
            }
        )

        objects = search.query(query)

        for item in objects:
            response_list.append(map_response_item(item))

    return response_list


def map_response_item(item):
    if item.meta.index == "cities":
        return {"name": item.name, "region": item.region}
    elif item.meta.index == "clubs":
        return {
            "name": item.name,
            "description": item.description,
            "contact_email": item.contact_email,
            "pricing": item.pricing,
            "register_info": item.register_info,
        }
    elif item.meta.index == "groups":
        return {
            "name": item.name,
            "description": item.description,
            "cover_photo": item.cover_photo,
            "contact_email": item.contact_email,
        }
    elif item.meta.index == "sports":
        return {"name": item.name}
    else:
        return
