from tastypie.test import TestApiClient
import json
from datetime import date, timedelta
from django.test import TestCase

class ListItTestCase(TestCase):
  def setUp(self):
      self.client = TestApiClient()

  def test_add_tasks(self):
      due_date = date.today() - timedelta(days=2)
      for i in range(16):

          response = self.client.post('/api/v1/tasks/', data={
              'title': 'test task',
              'due_date': due_date,
              'status': 'Pending'
              }
          )
          due_date = due_date + timedelta(days=1)
          self.assertEqual(response.status_code, 201)
