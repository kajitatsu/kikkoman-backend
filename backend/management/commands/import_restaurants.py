import csv
from backend.models import Restaurant  # アプリ名に注意
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'CSVファイルからRestaurantデータを一括インポート'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        with open(file_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                Restaurant.objects.create(
                    name=row['name'],
                    address=row['address'],
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    access_info=row.get('access_info', ''),
                    commercial_facility_id=row.get('commercial_facility') or None,
                    retty_id=row.get('retty_id', ''),
                    nursing_room=row.get('nursing_room', 'false').lower() == 'true',
                    diaper_changing_room=row.get('diaper_changing_room', 'false').lower() == 'true',
                    stroller=row.get('stroller', 'false').lower() == 'true',
                    baby_chair=row.get('baby_chair', 'false').lower() == 'true',
                    baby_food=row.get('baby_food', 'false').lower() == 'true',
                    baby_food_allowed=row.get('baby_food_allowed', 'false').lower() == 'true',
                    parking=row.get('parking', 'false').lower() == 'true',
                    sunken_kotatsu=row.get('sunken_kotatsu', 'false').lower() == 'true',
                    kids_menu=row.get('kids_menu', 'false').lower() == 'true',
                    kids_discount=row.get('kids_discount', 'false').lower() == 'true',
                    toys_given=row.get('toys_given', 'false').lower() == 'true',
                    allergy_friendly=row.get('allergy_friendly', 'false').lower() == 'true',
                    infants_allowed=row.get('infants_allowed', 'false').lower() == 'true',
                    preschoolers_allowed=row.get('preschoolers_allowed', 'false').lower() == 'true',
                    elementary_schoolers_allowed=row.get('elementary_schoolers_allowed', 'false').lower() == 'true',
                    play_zone=row.get('play_zone', 'false').lower() == 'true',
                    daycare_facility=row.get('daycare_facility', 'false').lower() == 'true',
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'{count} 件のレストランをインポートしました。'))
