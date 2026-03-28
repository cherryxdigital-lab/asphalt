from django.test import TestCase
from django.urls import reverse

from .models import EvacuatorOffer, EvacuatorSection


class HomePageEvacuatorTests(TestCase):
    def setUp(self):
        EvacuatorSection.objects.create(
            eyebrow="Евакуація техніки",
            title="Евакуатор для міста та області",
            description="Тестовий опис секції евакуатора.",
            cta_text="Замовити евакуатор",
        )
        EvacuatorOffer.objects.create(
            name="Малий евакуатор",
            subtitle="Тестова картка",
            description="Тестовий опис картки евакуатора.",
            price_text="від 3 000 грн",
            order=1,
        )

    def test_home_page_renders_evacuator_section(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Евакуатор для міста та області")
        self.assertContains(response, "Малий евакуатор")
