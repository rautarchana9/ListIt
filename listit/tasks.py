from background_task import background
from datetime import datetime, timedelta
from listit.models import Task

@background(schedule=60)
def delete_outdated_tasks():
    Task.all_objects.filter(deleted_at__lte=datetime.now()- timedelta(days=30) ).hard_delete()

delete_outdated_tasks()
