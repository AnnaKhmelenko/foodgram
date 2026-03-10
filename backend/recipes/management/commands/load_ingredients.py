import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из CSV файла'

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[3]
        csv_path = base_dir / 'data' / 'ingredients.csv'

        if not csv_path.exists():
            self.stdout.write(
                self.style.ERROR(f'Файл не найден: {csv_path}')
            )
            return

        ingredients_to_create = []

        with open(csv_path, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) != 2:
                    continue

                name, measurement_unit = row
                ingredients_to_create.append(
                    Ingredient(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
                )

        Ingredient.objects.bulk_create(
            ingredients_to_create,
            ignore_conflicts=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Загрузка завершена. Добавлено ингредиентов: '
                f'{len(ingredients_to_create)}'
            )
        )
