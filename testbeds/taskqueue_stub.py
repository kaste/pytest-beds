import base64, datetime

from google.appengine.api.taskqueue import taskqueue
from google.appengine.ext import deferred

class NothingToDo(Exception):    pass

class TaskqueueStub(object):
    def __init__(self, taskqueue):
        self.taskqueue = taskqueue

    def consume(self):
        while 1:
            try:
                self.tick()
            except NothingToDo:
                break

    def tick(self):
        tasks = self.get_filtered_tasks()
        if not tasks:
            raise NothingToDo()

        for task in tasks:
            try:
                deferred.run(task.payload)
            except deferred.PermanentTaskFailure:
                pass
            finally:
                self.taskqueue.DeleteTask(task.queue_name or 'default', task.name)

    def count_tasks(self):
        return len(self.get_filtered_tasks())

    def get_filtered_tasks(self, url=None, name=None, queue_names=None):
        return get_filtered_tasks(self.taskqueue, url, name, queue_names)

# patched version which sets the correct queue_name
# see: https://code.google.com/p/googleappengine/issues/detail?id=10848
def get_filtered_tasks(taskqueue_stub, url=None, name=None, queue_names=None):
    """Get the tasks in the task queue with filters.

    Args:
        url: A URL that all returned tasks should point at.
        name: The name of all returned tasks.
        queue_names: A list of queue names to retrieve tasks from. If left blank
            this will get default to all queues available.

    Returns:
        A list of taskqueue.Task objects.
    """
    all_queue_names = [queue['name'] for queue in taskqueue_stub.GetQueues()]

    if isinstance(queue_names, basestring):
        queue_names = [queue_names]


    if queue_names is None:
        queue_names = all_queue_names


    task_dicts = []
    for queue_name in queue_names:
        if queue_name in all_queue_names:
            for task in taskqueue_stub.GetTasks(queue_name):
                if url is not None and task['url'] != url:
                    continue
                if name is not None and task['name'] != name:
                    continue
                task_dicts.append(task)

    tasks = []
    for task in task_dicts:

        payload = base64.b64decode(task['body'])

        headers = dict(task['headers'])
        headers['Content-Length'] = str(len(payload))

        eta = datetime.datetime.strptime(task['eta'], '%Y/%m/%d %H:%M:%S')
        eta = eta.replace(tzinfo=taskqueue._UTC)

        task_object = taskqueue.Task(name=task['name'], method=task['method'],
                                     url=task['url'], headers=headers,
                                     payload=payload, eta=eta)
        # supercool to user super-private names here
        task_object._Task__queue_name = task['queue_name']
        tasks.append(task_object)
    return tasks
