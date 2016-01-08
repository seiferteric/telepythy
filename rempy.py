#!/usr/bin/python

import subprocess
import inspect
import StringIO
import pickle

class Remote(object):
    def __init__(self, host):
        self.host = host

    def run(self, func, *args, **kwargs):
        code = inspect.getsource(func)
        code += """
import sys, os
import pickle
args = pickle.loads(\"\"\"{1}\"\"\")
kwargs = pickle.loads(\"\"\"{2}\"\"\")
save_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
ret = pickle.dumps({0}(*args, **kwargs))
sys.stdout = save_stdout
print ret
""".format(func.__name__, pickle.dumps(args), pickle.dumps(kwargs))
        pinput = StringIO.StringIO(code)
        p = subprocess.Popen(['ssh', self.host, 'python'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output, output_err = p.communicate(pinput.read())
        return pickle.loads(output)

