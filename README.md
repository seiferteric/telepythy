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

#Example:

```python
from telepythy import Remote

s = Remote("myserver")

def doremotething(arg1, arg2='/'):
    import os
    return os.listdir(arg2), arg1

try:
    print s.run(doremotething, "myarg", arg2="/usr")
except:
    print 'I even handle remote exceptions!'

```

#TODO:

- Use paramiko, open multiple channels to leave stdout/stdin intact and pass
  args/return data back over another channel.
- Accept password authentication.
- Maybe enable remote file access with some sort of RemoteFile object?
