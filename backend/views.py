from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant
from django.db.models import Q
import json

@csrf_exempt
def all_restaurants(request):
    if request.method == "GET":
        restaurants = Restaurant.objects.all().values()
        return JsonResponse(list(restaurants), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

# Create your views here.


@csrf_exempt
def search_restaurants(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            freeword = data.get("freeword", "")
            features = data.get("features", [])

            queryset = Restaurant.objects.all()

            # フリーワード検索（店名 or アクセス情報に含まれる）
            if freeword:
                queryset = queryset.filter(
                    Q(name__icontains=freeword) |
                    Q(access_info__icontains=freeword)
                )

            # こだわり条件による絞り込み
            feature_field_map = {
                "授乳室あり": "nursing_room",
                "おむつ替え室あり": "diaper_changing_room",
                "ベビーカーあり": "stroller",
                "ベビーチェアあり": "baby_chair",
                "離乳食あり": "baby_food",
                "離乳食持込可": "baby_food_allowed",
                "駐車場あり": "parking",
                "掘りごたつあり": "sunken_kotatsu",
                "お子様ランチあり": "kids_menu",
                "お子様割引あり": "kids_discount",
                "おもちゃがもらえる": "toys_given",
                "アレルギー対応可": "allergy_friendly",
            }

            for feature in features:
                field_name = feature_field_map.get(feature)
                if field_name:
                    queryset = queryset.filter(**{field_name: True})

            restaurants = queryset.values()
            return JsonResponse(list(restaurants), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def search_by_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = float(data.get("latitude", 0))
            longitude = float(data.get("longitude", 0))

            radius_meters = 5000  # 半径5km

            def haversine(lat1, lon1, lat2, lon2):
                from math import radians, sin, cos, sqrt, atan2
                R = 6371000  # 地球の半径(m)
                dlat = radians(lat2 - lat1)
                dlon = radians(lon2 - lon1)
                a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                return R * c

            all_restaurants = Restaurant.objects.all()
            nearby = [
                r for r in all_restaurants
                if haversine(latitude, longitude, r.latitude, r.longitude) <= radius_meters
            ]

            return JsonResponse([{
                "id": r.id,
                "name": r.name,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "address": r.address,
                "access": r.access_info,
                "hours": "",  # 必要ならモデルに追加
                "imageUrl": "",  # 必要なら画像URLフィールドに追加
            } for r in nearby], safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def restaurant_count(request):
    if request.method == "GET":
        count = Restaurant.objects.count()
        return JsonResponse({"count": count})
    return JsonResponse({"error": "Invalid request method"}, status=400)