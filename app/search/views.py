from django.http import HttpResponse

from elasticsearch_dsl import Q, Search, utils
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
        json.dumps(
            {"count": 0, "next": None, "previous": None, "results": response_list},
            default=obj_dict,
        ),
        status=200,
        content_type="application/json",
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
        return {"id": item.id, "name": item.name, "region": item.region}
    elif item.meta.index == "clubs":
        return {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "contact_email": item.contact_email,
            "membership_fee": item.membership_fee,
            "register_info": item.register_info,
            "city": item.city,
        }
    elif item.meta.index == "groups":
        if not item.cover_photo:
            item.cover_photo = None
        return {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "cover_photo": item.cover_photo,
            "contact_email": item.contact_email,
            "city": item.city,
            "sports": item.sports,
            "club": item.club,
        }
    elif item.meta.index == "sports":
        return {"id": item.id, "name": item.name}
    else:
        return


def obj_dict(obj):
    """
    :param obj: An elasticsearch AttrList or AttrDict
    :return: A list or dictionary to match the model in django
    """

    if isinstance(obj, utils.AttrList):
        values = []
        for item in obj.__dict__["_l_"]:
            values.append(item["id"])
        return values
    elif obj.__contains__("id"):
        return obj.to_dict()["id"]
    return None
