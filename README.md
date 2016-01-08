# rempy
Remote Python Runner

This is an experimental library to make it easy to run python scripts on remote
machines you have ssh access to.

After you create a Remote object, you can use the run method to pass a function
you want to run on the remote machine. The method can take arguments and return
arguments as normal. Since rempy uses pickle to marshal the arguments and
return values, they must be picklable objects.

#Example:

```python
from rempy import Remote

s = Remote("myserver")

def doremotething(arg1, arg2='/'):
    import os
    return os.listdir(arg2), arg1


ret = s.run(doremotething, "myarg", arg2="/usr")

print ret
```


#TODO:

- Use paramiko, open multiple channels to leave stdout/stdin intact and pass
  args/return data back over another channel.
- Accept password authentication.
- Maybe enable remote file access with some sort of RemoteFile object?
