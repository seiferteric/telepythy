#!/usr/bin/python

import subprocess
import inspect
import pickle
import paramiko


class Remote(object):
    def __init__(self, host, username=None, password=None, key_filename=None):
        self.host = host
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.host,
            username=username,
            password=password,
            key_filename=key_filename
        )

    def close(self):
        self.ssh.close()

    def run(self, func, *args, **kwargs):
        code = inspect.getsource(func) + "\n"
        code += inspect.getsource(_wrapper_function).format(
               func.__name__,
               pickle.dumps(args),
               pickle.dumps(kwargs),
            )
        code += "\n_wrapper_function()\n"
        si, so, sr = self.ssh.exec_command('python')
        si.write(code)
        si.flush()
        si.channel.shutdown_write()
        output = so.read()
        ret = pickle.loads(output)
        if isinstance(ret, Exception):
            raise ret
        return ret


def _wrapper_function():
    import sys
    import os
    import pickle
    args = pickle.loads("""{1}""")
    kwargs = pickle.loads("""{2}""")
    save_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        ret = pickle.dumps({0}(*args, **kwargs))
    except Exception as e:
        ret = pickle.dumps(e)
    sys.stdout = save_stdout
    print ret
