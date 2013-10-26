"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from photography.models import Photograph

class PhotographyTestCase(TestCase):
  def setUp(self):
    pass
    
  def test_always_works(self):
    self.assertEqual(2, 1 + 1) 
