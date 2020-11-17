import json
from recipes.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('ingredients.json', 'r', encoding='utf-8') as fh:
            data = json.load(fh)

        for i in data:
            dimension = i['dimension']
            title = i['title']

            if not Ingredient.objects.filter(title=title).exists():
                print(f'Добавляю {title}')
                if dimension in ['по вкусу', 'стакан', 'кусок',
                                 'горсть', 'банка', 'тушка', 'пакет']:
                    dimension = 'г'
                ingredient = Ingredient(title=title, dimension=dimension)
                ingredient.save()

        return '--Ингредиенты добавлены--'
