from django.core.management.base import BaseCommand
from landing.models import EquipmentRental, AsphaltType
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **options):
        # Очистка
        EquipmentRental.objects.all().delete()
        AsphaltType.objects.all().delete()

        # Аренда техники
        EquipmentRental.objects.create(
            name='Каток 5 тонн',
            description='Каток для уплотнения асфальта, вес 5 тонн.',
            price=Decimal('7000'),
            price_unit='смена (8 часов)'
        )

        EquipmentRental.objects.create(
            name='Каток 3-5 тонн',
            description='Каток для уплотнения асфальта, вес 3-5 тонн.',
            price=Decimal('7000'),
            price_unit='смена (8 часов)'
        )

        EquipmentRental.objects.create(
            name='Асфальтоукладчик',
            description='Машина для укладки асфальта.',
            price=Decimal('25000'),
            price_unit='смена (8 часов)'
        )

        EquipmentRental.objects.create(
            name='Экскаватор',
            description='Экскаватор для земляных работ.',
            price=Decimal('1300'),
            price_unit='час',
            min_hours=4
        )

        EquipmentRental.objects.create(
            name='Мини-экскаватор',
            description='Мини-экскаватор для точных работ.',
            price=Decimal('1200'),
            price_unit='час',
            min_hours=4
        )

        EquipmentRental.objects.create(
            name='Каток 10 тонн',
            description='Каток для уплотнения асфальта, вес 10 тонн.',
            price=Decimal('10000'),
            price_unit='смена (8 часов)'
        )

        EquipmentRental.objects.create(
            name='Бабкет с гидромолотом',
            description='Бабкет с гидромолотом для демонтажа.',
            price=Decimal('1300'),
            price_unit='час',
            min_hours=4
        )

        # Типы асфальта
        AsphaltType.objects.create(
            name='Асфальт стандартный',
            description='Стандартный асфальт для дорог. Цена от 600 до 1500 грн/кв.м.',
            price_per_sqm=Decimal('600')
        )

        AsphaltType.objects.create(
            name='Асфальтная крошка',
            description='Асфальтная крошка для ямочного ремонта. 350 грн/кв.м.',
            price_per_sqm=Decimal('350')
        )

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены!'))