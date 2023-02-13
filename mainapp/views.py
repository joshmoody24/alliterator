from django.shortcuts import render, redirect
from django.http import HttpResponse
from .scraper import getSynonyms, getAlliterations

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def alliterator(request):
    return render(request, "alliterator.html")

def submit(request):
    if(request.method != "POST"):
        return HttpResponse("No form data detected")
    
    word1 = request.POST.get('word1')
    word2 = request.POST.get('word2')
    if(word1 == '' or word2 == ''):
        return redirect(request.POST.get('origin'))
    return redirect('results', word1=word1.lower(), word2=word2.lower())

def error(request, message):
    context = { "message": message }
    return render(request, "error.html", context)

def results(request, word1='', word2=''):

    # convert the words into alliterations
    try:
        synonyms1 = getSynonyms(word1)
        synonyms2 = getSynonyms(word2)
        alliterations = getAlliterations(synonyms1, synonyms2)
    except Exception as e:
        return redirect("error", str(e))
    # sort the alliterations alphabetically
    alliterations = {key: alliterations[key] for key in sorted(alliterations)}


    context = {
        'word1': word1,
        'word2': word2,
        'alliterations': alliterations,
    }
    return render(request, "results.html", context)
