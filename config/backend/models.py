from django.db import models

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="店舗名")
    address = models.TextField(verbose_name="住所")
    latitude = models.FloatField(verbose_name="緯度")
    longitude = models.FloatField(verbose_name="経度")
    access_info = models.TextField(null=True, blank=True, verbose_name="アクセス情報")
    commercial_facility = models.ForeignKey(
        'CommercialFacility',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="商業施設"
    )
    nursing_room = models.BooleanField(default=False, verbose_name="授乳室")
    diaper_changing_room = models.BooleanField(default=False, verbose_name="おむつ替え室")
    stroller = models.BooleanField(default=False, verbose_name="ベビーカー")
    baby_chair = models.BooleanField(default=False, verbose_name="ベビーチェア")
    baby_food = models.BooleanField(default=False, verbose_name="離乳食")
    baby_food_allowed = models.BooleanField(default=False, verbose_name="離乳食持ち込み可")
    parking = models.BooleanField(default=False, verbose_name="駐車場")
    sunken_kotatsu = models.BooleanField(default=False, verbose_name="掘り炬燵")
    kids_menu = models.BooleanField(default=False, verbose_name="お子様ランチ")
    kids_discount = models.BooleanField(default=False, verbose_name="お子様割引有無")
    toys_given = models.BooleanField(default=False, verbose_name="おもちゃがもらえる")
    allergy_friendly = models.BooleanField(default=False, verbose_name="アレルギー対応可")

    class Meta:
        verbose_name = "レストラン情報"
        verbose_name_plural = "レストラン情報"

    def __str__(self):
        return self.name


class CommercialFacility(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="施設名")
    address = models.TextField(verbose_name="住所")
    latitude = models.FloatField(verbose_name="緯度")
    longitude = models.FloatField(verbose_name="経度")
    access_info = models.TextField(null=True, blank=True, verbose_name="アクセス情報")
    nursing_room = models.BooleanField(default=False, verbose_name="授乳室")
    diaper_changing_room = models.BooleanField(default=False, verbose_name="おむつ替え室")
    stroller = models.BooleanField(default=False, verbose_name="ベビーカー")
    baby_chair = models.BooleanField(default=False, verbose_name="ベビーチェア")
    parking = models.BooleanField(default=False, verbose_name="駐車場")
    kids_discount = models.BooleanField(default=False, verbose_name="お子様割引有無")

    class Meta:
        verbose_name = "商業施設情報"
        verbose_name_plural = "商業施設情報"

    def __str__(self):
        return self.name