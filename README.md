# taskscheduler
A python task scheduler similar to Timer in C++

Scheduler can be add task to be scheduled periodly after given delay, or run first time at specified time, then run repeatly (or not repeatly)

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
s.add_task(cancel_task, args=(scheduler, id), delay=20)

```
