from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant
from .utils import haversine
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
                "乳幼児可": "infants_allowed",
                "未就学児可": "preschoolers_allowed",
                "小学生可": "elementary_schoolers_allowed",
                "授乳室あり": "nursing_room",
                "おむつ台あり": "diaper_change",
                "ベビーカーあり": "stroller",
                "ベビーチェアあり": "baby_chair",
                "離乳食あり": "baby_food",
                "離乳食持込可": "baby_food_ok",
                "駐車場あり": "parking",
                "掘りごたつあり": "horigotatsu",
                "プレイゾーンあり": "play_zone",
                "託児施設あり": "daycare_facility",
                "お子様メニューあり": "kids_lunch",
                "お子様割引あり": "kids_discount",
                "おもちゃがもらえる": "toy_present",
                "アレルギー食対応可": "allergy_ok",
                "タンパク質がとれる": "protein_rich",
                "野菜が好きになる": "vegetable_like",
                "野菜が食べれる": "vegetable_rich",
                "減塩メニューあり": "low_salt",
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

            radius_km = 5.0  # 半径5km（km単位に統一）

            all_restaurants = Restaurant.objects.all()
            nearby = [
                {
                    "restaurant": r,
                    "distance": haversine(latitude, longitude, float(r.latitude), float(r.longitude))
                }
                for r in all_restaurants
                if r.latitude is not None and r.longitude is not None and
                    haversine(latitude, longitude, float(r.latitude), float(r.longitude)) <= radius_km
            ]

            # 距離でソート
            nearby.sort(key=lambda x: x["distance"])

            return JsonResponse([{
                "id": r["restaurant"].id,
                "name": r["restaurant"].name,
                "latitude": r["restaurant"].latitude,
                "longitude": r["restaurant"].longitude,
                "address": r["restaurant"].address,
                "access": r["restaurant"].access_info,
                "retty_id": r["restaurant"].retty_id,
                "hours": "",  # 必要に応じて修正
                "imageUrl": "",  # 必要に応じて修正
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



@csrf_exempt
def search_with_location_and_filters(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            freeword = data.get("freeword", "")
            features = data.get("features", [])
            latitude = float(data.get("latitude"))
            longitude = float(data.get("longitude"))

            feature_field_map = {
                "乳幼児可": "infants_allowed",
                "未就学児可": "preschoolers_allowed",
                "小学生可": "elementary_schoolers_allowed",
                "授乳室あり": "nursing_room",
                "おむつ台あり": "diaper_change",
                "ベビーカーあり": "stroller",
                "ベビーチェアあり": "baby_chair",
                "離乳食あり": "baby_food",
                "離乳食持込可": "baby_food_ok",
                "駐車場あり": "parking",
                "掘りごたつあり": "horigotatsu",
                "プレイゾーンあり": "play_zone",
                "託児施設あり": "daycare_facility",
                "お子様メニューあり": "kids_lunch",
                "お子様割引あり": "kids_discount",
                "おもちゃがもらえる": "toy_present",
                "アレルギー食対応可": "allergy_ok",
                "タンパク質がとれる": "protein_rich",
                "野菜が好きになる": "vegetable_like",
                "野菜が食べれる": "vegetable_rich",
                "減塩メニューあり": "low_salt",
            }

            # 全店舗から半径5km以内にあるものを絞り込み
            all_restaurants = Restaurant.objects.all()
            nearby_restaurants = [
                {
                    "restaurant": r,
                    "distance": haversine(latitude, longitude, float(r.latitude), float(r.longitude))
                }
                for r in all_restaurants
                if r.latitude is not None and r.longitude is not None and
                    haversine(latitude, longitude, float(r.latitude), float(r.longitude)) <= 5
            ]

            # 距離でソート
            nearby_restaurants.sort(key=lambda x: x["distance"])

            # クエリセットとして扱うためにフィルタリング
            queryset = Restaurant.objects.filter(id__in=[r["restaurant"].id for r in nearby_restaurants])

            # フリーワード検索
            if freeword:
                queryset = queryset.filter(
                    Q(name__icontains=freeword) |
                    Q(access_info__icontains=freeword)
                )

            # こだわり条件
            for feature in features:
                field_name = feature_field_map.get(feature)
                if field_name:
                    queryset = queryset.filter(**{field_name: True})

            return JsonResponse(list(queryset.values()), safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)