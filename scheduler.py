# encoding: utf-8

# a timer to add task which can be executed periodly after given delay
import threading
from datetime import datetime, timedelta
from typing import Callable


class Task:
    def __init__(self, id: int, func: Callable, args=(), kwargs=None, interval=None, delay=None):
        self.id = id
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.interval = interval
        self.delay = delay
        self.timer = None


class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.next_id = 0

    def add_task(self, event_time, func: Callable, args=(), kwargs=None, interval=None) -> int:
        task_id = self.next_id
        first_act = None
        delay = None
        _now = datetime.now()
        if isinstance(event_time, str):
            first_act = datetime.strptime(event_time, '%H:%M:%S')
        elif isinstance(event_time, datetime):
            first_act = event_time
        elif isinstance(event_time, (int, timedelta)):
            # if not specified time, treat as delay
            if isinstance(event_time, int):
                delay = timedelta(microseconds=event_time)
            else:
                delay = event_time
        else:
            return

        if delay is None:
            delay = first_act - _now

        delay_seconds = delay.total_seconds()
        if delay_seconds < 0:
            delay_seconds = 0

        # given in microseconds
        interval_seconds = 0
        if interval is not None:
            if isinstance(interval, (int, float)):
                period = timedelta(microseconds=interval)
            elif not isinstance(interval, (timedelta, )):
                period = timedelta(0)
            else:
                period = interval
            
            interval_seconds = period.total_seconds()

        task = Task(task_id, func, args=args, kwargs=kwargs, interval=interval_seconds, delay=delay_seconds)
        self.tasks.append(task)
        if task.delay:
            if task.interval is None:
                task.timer = threading.Timer(task.delay, task.func, args=task.args, kwargs=task.kwargs)
                task.timer.start()
            else:
                task.timer = threading.Timer(task.delay, self._run_periodic_task, args=(task, ))
                task.timer.start()
        else:
            task.timer = threading.Timer(0, self._run_periodic_task, args=(task, ))
            task.timer.start()

        # Increment next_id for next added task.
        self.next_id += 1

        return task_id

    def _run_periodic_task(self, task: Task):
        if not task.timer:
            return
        task.func(*task.args, **task.kwargs)
        task.timer = threading.Timer(task.interval, self._run_periodic_task, args=(task, ))
        task.timer.start()

    def cancel_task(self, id: int):
        for i in range(len(self.tasks)):
            if id == self.tasks[i].id:
                if not self.tasks[i].timer:
                    return
                else:
                    # Cancel timer and remove from tasks list.
                    self.tasks[i].timer.cancel()
                    del self.tasks[i]
                    break


"""  example:

def my_func(arg1,arg2):
    print(f'arg1: {arg1}, arg2: {arg2}')

def cancel_task(sched, id):
    sched.cancel_task(id)
    
scheduler = TaskScheduler()
id = scheduler.add_task(event_time, my_func,args=('hello','world'),interval=5)
scheduler.add_task(cancel_task, args=(scheduler, id), delay=20)

"""
