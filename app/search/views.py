from django.shortcuts import render
from search.documents import ClubDocument

# Create your views here.
def search(request):
    q = request.GET.get('q')

    if q:
        clubs = ClubDocument.search().query("match", name=q)
        print(q)
    else:
        clubs = ''
        print("hva og Q:", q)

    return render(request, 'search/search.html', {'clubs': clubs})