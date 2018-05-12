from tastypie.test import TestApiClient, ResourceTestCaseMixin  
import json
from datetime import date, timedelta
from django.test import TestCase
from listit.models import Task

class ListItTestCase(ResourceTestCaseMixin, TestCase):
  def setUp(self):
    super(ListItTestCase, self).setUp()  
    self.client = TestApiClient()

  def test_add_tasks(self):
    #curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"title": "test task 9", "due_date":"2018-05-22T00:46:38", "status": "P" }' http://localhost:8000/api/v1/tasks/
    due_date = date.today() - timedelta(days=2)
    for i in range(16):

        response = self.client.post('/api/v1/tasks/', data={
            'title': 'test task',
            'due_date': due_date,
            'status': 'P',
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
  

  def test_search_known_tasks(self):
    #http://127.0.0.1:8000/api/v1/tasks/search/?format=json&q=test task 6
    self.test_add_tasks()
    response = self.client.get('/api/v1/tasks/search/?q=test task')
    response_obj = response.json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response_obj.get('objects')), 16)

  def test_search_unknown_tasks(self):
    #http://127.0.0.1:8000/api/v1/tasks/search/?format=json&q=test task 6
    self.test_add_tasks()
    response = self.client.get('/api/v1/tasks/search/?q=blah')
    response_obj = response.json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response_obj.get('objects')), 0)

  def test_get_task_detail_json(self):
    self.test_filter_today_tasks()
    response = self.api_client.get('/api/v1/tasks/1/', format='json')
    self.assertValidJSONResponse(response)
    self.assertKeys(self.deserialize(response), ['title', 'due_date', 'status', 'resource_uri'])
    self.assertEqual(self.deserialize(response)['title'], 'test task')
    self.assertEqual(self.deserialize(response)['status'], 'P')
    self.assertEqual(self.deserialize(response)['due_date'], ( (date.today() - timedelta(days=2) ).isoformat() ) )
 
  def test_put_detail(self):
    # Grab the current data & modify it slightly.
    self.test_add_tasks()
    original_data = self.deserialize(self.api_client.get('/api/v1/tasks/1/', format='json'))
    new_data = original_data.copy()
    new_data['status'] = 'C'
    self.assertEqual(Task.objects.count(), 16)
    self.assertHttpAccepted(self.api_client.put('/api/v1/tasks/1/', format='json', data=new_data))
    # Make sure the count hasn't changed & we did an update.
    self.assertEqual(Task.objects.count(), 16)
    # Check for updated data.
    self.assertEqual(Task.objects.get(pk=1).status, 'C')
    

