from django.db import migrations


def refresh_evacuator_content(apps, schema_editor):
    EvacuatorSection = apps.get_model('landing', 'EvacuatorSection')
    EvacuatorOffer = apps.get_model('landing', 'EvacuatorOffer')

    section = EvacuatorSection.objects.order_by('id').first()
    if section:
        section.eyebrow = 'Доставка техніки та евакуація'
        section.title = 'Евакуатор для перевезення техніки на об’єкт і окремих виїздів для авто'
        section.description = (
            'Коли замовляють техніку для асфальтних робіт, ми допомагаємо організувати її доставку '
            'евакуатором на об’єкт. Окремо також приймаємо замовлення на евакуацію легкових авто, '
            'кросоверів, бусів і комерційного транспорту по місту та за його межами.'
        )
        section.cta_text = 'Замовити евакуатор'
        section.show_on_site = True
        section.save()

    updates = {
        'Малий евакуатор': {
            'subtitle': 'Швидка подача для легкових авто та компактних кросоверів',
            'description': (
                'Підходить для міських виїздів, доставки авто на СТО та акуратного завантаження '
                'машин з низькою посадкою. Також може використовуватись для локальної логістики '
                'невеликої техніки на об’єкт.'
            ),
            'price_text': 'від 3 000 грн',
            'featured': False,
            'show_on_site': True,
            'order': 10,
        },
        'Великий евакуатор': {
            'subtitle': 'Для важчої техніки, бусів і складних завантажень',
            'description': (
                'Потрібен, коли треба перевезти більшу техніку на об’єкт асфальтування або '
                'евакуювати комерційний транспорт. По місту від 6 000 грн, виїзд за межі міста '
                'прораховується окремо залежно від маршруту.'
            ),
            'price_text': 'від 6 000 грн',
            'featured': True,
            'show_on_site': True,
            'order': 20,
        },
        'Евакуатор за місто': {
            'subtitle': 'Міжміські виїзди та евакуація по області',
            'description': (
                'Якщо техніку або авто потрібно забрати з траси, селища чи сусіднього міста, '
                'погоджуємо маршрут заздалегідь і називаємо вартість до виїзду. Базова ставка '
                'по місту від 6 000 грн, за місто обговорюється окремо.'
            ),
            'price_text': '6 000 грн, за місто обговорюється',
            'featured': False,
            'show_on_site': True,
            'order': 30,
        },
    }

    for name, payload in updates.items():
        EvacuatorOffer.objects.filter(name=name).update(**payload)


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_evacuatoroffer_evacuatorsection'),
    ]

    operations = [
        migrations.RunPython(refresh_evacuator_content, migrations.RunPython.noop),
    ]
