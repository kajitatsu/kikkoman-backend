from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant
import json

@csrf_exempt
def all_restaurants(request):
    if request.method == "POST":
        restaurants = Restaurant.objects.all().values()
        return JsonResponse(list(restaurants), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Create your views here.
