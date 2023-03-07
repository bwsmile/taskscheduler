# taskscheduler
A python task scheduler similar to Timer in C++

Scheduler can be add task:
1. to be scheduled periodly
2. to be scheduled periodly (or not) after given delay
3. to be scheduled at a specified time for first time, then run periodly (or not)

main interfaces:
``` python
1. def add_task(self, event_time, func: Callable, args=(), kwargs=None, interval=None) -> int  # event_time maybe delay(int), or timedelta, or a datetime
2. def cancel_task(self, id: int):
```

usage:
``` python
s = TaskScheduler()

def func(args, kwargs):
  print(f"task running: {args}, {kwargs})

def my_func(arg1,arg2):
    print(f'arg1: {arg1}, arg2: {arg2}')

def cancel_task(sched, id):
    sched.cancel_task(id)
    
id = s.add_task(0, my_func,args=('hello','world'),interval=5)
s.add_task(20, cancel_task, args=(scheduler, id))

```
