from django.test import TestCase


class HomeTestCase(TestCase):
    def test_get_context_data(self):
        response = self.client.get('/')
        self.assertIn('posts', response.context)
