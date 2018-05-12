from tastypie.test import TestApiClient, ResourceTestCaseMixin  
import json
from datetime import date, timedelta
from django.test import TestCase

class ListItTestCase(TestCase):
  def setUp(self):
      self.client = TestApiClient()

  def test_add_tasks(self):
    #curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"title": "test task 9", "due_date":"2018-05-22T00:46:38", "status": "Pending" }' http://localhost:8000/api/v1/tasks/
    due_date = date.today() - timedelta(days=2)
    for i in range(16):

        response = self.client.post('/api/v1/tasks/', data={
            'title': 'test task',
            'due_date': due_date,
            'status': 'Pending',
            }
        )
        due_date = due_date + timedelta(days=1)
        self.assertEqual(response.status_code, 201)

  def test_filter_today_tasks(self):
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

  def test_filter_overdue_tasks(self):
    self.test_add_tasks()
    response = self.client.get('/api/v1/filters/', data={"duedate":"overdue"})
    response_obj = response.json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response_obj.get('objects')),2)

  def test_add_subtask(self):
    self.test_filter_today_tasks()
   # curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"title": "test task ", "task": "/api/v1/tasks/9/" }' http://localhost:8000/api/v1/subtasks/ 
    response = self.client.post('/api/v1/subtasks/', data={
        'title': 'test subtask',
        'task': '/api/v1/tasks/1/',
        }
    )
    self.assertEqual(response.status_code, 201)
#class TaskResourceTest(ResourceTestCaseMixin, TestCase):
#
#  def test_search_tasks(self):
#    response = self.api_client.get('/api/v1/tasks/search', format = 'json')
#    self.assertValidJSONResponse(response)

