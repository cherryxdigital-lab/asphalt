from landing.models import EquipmentRental, AsphaltType, BlogPost
from decimal import Decimal

# Очистка
EquipmentRental.objects.all().delete()
AsphaltType.objects.all().delete()
BlogPost.objects.all().delete()

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

# Статьи блога
BlogPost.objects.create(
    title='Технології укладання асфальту: сучасні методи',
    slug='tekhnolohii-ukladannia-asfaltu-suchasni-metody',
    short_description='Дізнайтеся про найновітніші технології укладання асфальтового покриття, які забезпечують довговічність та якість.',
    full_description='''<p>Сучасні технології укладання асфальту значно відрізняються від традиційних методів. Використання спеціального обладнання та матеріалів дозволяє досягти високої якості покриття.</p>

<p><strong>Основні етапи укладання:</strong></p>
<ul>
<li>Підготовка основи</li>
<li>Укладання нижнього шару</li>
<li>Укладання верхнього шару</li>
<li>Уплотнення катками</li>
</ul>

<p>Правильна технологія гарантує довговічність асфальтового покриття до 15 років.</p>''',
    image_url='https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
)

BlogPost.objects.create(
    title='Чому важливо вибирати якісний асфальт',
    slug='chomu-vazhlyvo-vybyraty-yakisnyy-asfalt',
    short_description='Якісний асфальт - запорука безпеки та комфорту. Розповідаємо про критерії вибору матеріалів.',
    full_description='''<p>Вибір якісного асфальту - це не тільки економія коштів, але й забезпечення безпеки дорожнього руху та комфорту користувачів.</p>

<p><strong>Критерії якості асфальту:</strong></p>
<ul>
<li>Стійкість до навантажень</li>
<li>Водостійкість</li>
<li>Зносостійкість</li>
<li>Шорсткість поверхні</li>
</ul>

<p>Наша компанія використовує тільки сертифіковані матеріали та сучасне обладнання.</p>''',
    image_url='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
)

BlogPost.objects.create(
    title='Ремонт асфальтового покриття: коли і як',
    slug='remont-asfaltovoho-pokryttia-koly-i-yak',
    short_description='Своєчасний ремонт асфальту дозволяє уникнути великих витрат та забезпечити безпеку руху.',
    full_description='''<p>Регулярний огляд та своєчасний ремонт асфальтового покриття - ключ до збереження його функціональності.</p>

<p><strong>Ознаки необхідності ремонту:</strong></p>
<ul>
<li>Виникнення тріщин</li>
<li>Поява вибоїн</li>
<li>Зниження шорсткості</li>
<li>Наявність калюж після дощу</li>
</ul>

<p>Наші спеціалісти проведуть діагностику та запропонують оптимальні рішення.</p>''',
    image_url='https://images.unsplash.com/photo-1581092160607-ee22621dd758?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
)

print('Данные добавлены!')