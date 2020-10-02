from django.http import HttpResponse
from django_elasticsearch_dsl.search import Search
from elasticsearch_dsl.query import MultiMatch

from rest_framework.utils import json
from elasticsearch_dsl import Search, Q

def global_search(request):
    q = request.GET.get('q')

    if q:
        search = Search(index=["clubs", "cities", "groups", "sports"])
        #query = MultiMatch(query=q, fields=["name", "description"], fuzziness="AUTO")
        query = Q({
            "multi_match": {
                "query": q,
                "fields": ["name", "description"],
                "fuzziness": "AUTO",
            }

        })
        objects = search.query(query)
        response_list = []

        for item in objects:
            if item.meta.index == "cities":
                response_list.append(
                    {
                        "name": item.name,
                        "region": item.region
                    }
                )
            elif item.meta.index == "clubs":
                response_list.append(
                    {
                        "name": item.name,
                        "description": item.description,
                        "contact_email": item.contact_email,
                        "pricing": item.pricing,
                        "register_info": item.register_info
                    }
                )
            elif item.meta.index == "groups":
                response_list.append(
                    {
                        "name": item.name,
                        "description": item.description,
                        "cover_photo": item.cover_photo,
                        "contact_email": item.contact_email
                    }
                )
            elif item.meta.index == "sports":
                response_list.append(
                    {
                        "name": item.name
                    }
                )

    else:
        response_list = []

    return HttpResponse(json.dumps(response_list), status=200, content_type="application/json")