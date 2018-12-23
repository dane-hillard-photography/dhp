from django.test import TestCase


class PortfolioTestCase(TestCase):
    def test_get_context_data(self):
        response = self.client.get('/portfolio')
        self.assertIn('photos', response.context)
