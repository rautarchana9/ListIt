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

  def test_fiter_today_tasks(self):
    self.test_add_tasks()
    response = self.client.get('/api/v1/filters/', data={"duedate":"today"})
    response_obj = response.json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response_obj.get('objects')),1)
  
  def test_filter_this_week_tasks(self):
    self.test_add_tasks()
    response = self.client.get('/api/v1/filters/', data={"duedate":"this_week"})
    response_obj = response.json()
    today = date.today()
    week_start = today - timedelta(days = today.weekday())
    end = week_start + timedelta(days = 6)
    count = (end - today).days + 1
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response_obj.get('objects')),count)
  def test_filter_next_week_tasks(self):
    self.test_add_tasks()
    response = self.client.get('/api/v1/filters/', data={"duedate":"next_week"})
    response_obj = response.json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response_obj.get('objects')),7)
    
