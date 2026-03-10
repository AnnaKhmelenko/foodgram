import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из data/ingredients.csv'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[4]
        file_path = base_dir / 'data' / 'ingredients.csv'

        if not file_path.exists():
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {file_path}')
            )
            return

        created_count = 0

        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            ingredients_to_create = []

            for row in reader:
                if len(row) != 2:
                    continue

                name, measurement_unit = row
                ingredients_to_create.append(
                    Ingredient(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                )

            created_objects = Ingredient.objects.bulk_create(
                ingredients_to_create,
                ignore_conflicts=True
            )
            created_count = len(created_objects)

        self.stdout.write(
            self.style.SUCCESS(
                f'Загрузка завершена. Добавлено ингредиентов: {created_count}'
            )
        )
