from django.shortcuts import render

def createPoolView(request):
    context = {}
    return render(request, "createPoolTemplate.html", context)
    