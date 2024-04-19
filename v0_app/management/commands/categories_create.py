from django.core.management import BaseCommand
from v0_app.models import Category, Recipe


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Category.objects.exists():
            print("Таблица с категориями уже существует")
        else:
            categories = [
                Category(name='first_dish', description='Все виды супов'),
                Category(name='main_dish', description='Основные "горячие" блюда'),
                Category(name='snacks', description='Салаты, холодные закуски'),
                Category(name='hot_snacks', description='Горячие закуски'),
                Category(name='deserts', description='Сладкие блюда, десерты, выпечка'),
                Category(name='other', description='Всё что не вошло в остальные категории')
            ]

            for category in categories:
                category.save()
            print('Таблица с категориями создана')