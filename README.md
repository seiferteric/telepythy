# telepythy
Remote Python Runner

This is an experimental library to make it easy to run python functions on
remote machines you have ssh access to. This is cool since you don't have
to resort to using shell functions to do your remote dirty work.

The intent of this library is to make interacting with remote systems easy
and with low mental overhead. You are just running a function in the
"context" of a remote machine. Nothing needs to be on the remote machine
except for python (and any libraries you intend to use).

After you create a Remote object, you can use the run method to pass a function
you want to run on the remote machine. The method can take arguments and return
arguments as normal. Since telepythy uses pickle to marshal the arguments and
return values, they must be picklable objects.

# Examples:

## Show contents of remote directory and handle possible exceptions:
```python
from telepythy import Remote

def do_remote_thing(dir='/'):
    import os
    print('I am remote!')
    return os.listdir(dir)

s = Remote('localhost')

try:
    dir_list = s.run(
        do_remote_thing,
        dir="/usr"
    )
except Exception as e:
    print('I even handle remote exceptions! %s'%e)

for dir in dir_list:
    print(dir)

```

## Doing distributed computing work:

```python
from telepythy import Remote
import random

def do_hard_work(seed):
    # Simulate long running task...
    import time
    import random
    time.sleep(random.randint(1,10))
    return seed+random.randint(1,100)

# Pretend we have 10 different remotes...
remotes = [Remote('localhost') for i in range(0,10)]
results = []
# Run remote jobs
for r in remotes:
    r.run_async(do_hard_work, random.randint(1,100))
# Collect Results
for r in remotes:
    results.append(r.return_async())
# Process results
total = sum(results)
print(f'Total: {total}')
```

# Install

```
sudo pip install git+https://github.com/seiferteric/telepythy.git
```
