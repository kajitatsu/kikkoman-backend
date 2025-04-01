from django.contrib import admin
from .models import Restaurant, CommercialFacility

# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "address", "retty_id", "latitude", "longitude", "access_info", 
        "commercial_facility", "nursing_room", "diaper_changing_room", 
        "stroller", "baby_chair", "baby_food", "baby_food_allowed", 
        "parking", "horigotatsu", "kids_menu", "kids_discount", 
        "toys_given", "allergy_friendly", "protein_rich", "vegetable_like",
        "vegetable_rich", "infants_allowed", "preschoolers_allowed",
        "elementary_schoolers_allowed", "play_zone", "daycare_facility"
    )  # 管理画面で表示するフィールド
    search_fields = ("name", "address")  # 検索可能なフィールド


@admin.register(CommercialFacility)
class CommercialFacilityAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "address", "latitude", "longitude", "access_info", 
        "nursing_room", "diaper_changing_room", "stroller", "baby_chair", 
        "parking", "kids_discount"
    )  # 管理画面で表示するフィールド
    search_fields = ("name", "address")  # 検索可能なフィールド