from background_task import background
from listit.models import Task

@background(schedule=60)
def test_task(task_id):
    task = Task.objects.get(pk=task_id)
    print(task.STATUS_TYPE)

test_task(4)
