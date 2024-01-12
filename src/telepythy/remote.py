#!/usr/bin/python
import subprocess
import inspect
import pickle
import paramiko
import sys
import os


class Remote(object):
    def __init__(self, host, username=None, password=None, key_filename=None):
        self.host = host
        self.ssh = paramiko.SSHClient()

        cfg = {
            'hostname': self.host,
            'username': username,
            'key_filename': key_filename,
            'password': password
        }

        # Check configuration file
        config = paramiko.SSHConfig()
        try:
            config.parse(open(os.path.expanduser('~/.ssh/config')))
        except:
            pass
        host = config.lookup(host)
        if 'proxycommand' in host:
            cfg['sock'] = paramiko.ProxyCommand(
                subprocess.check_output(
                    [os.environ['SHELL'], '-c', 'echo %s' % host['proxycommand']]
                ).strip()
            )
        else:
            cfg['sock'] = None

        if 'hostname' in host:
            cfg['hostname'] = host['hostname']
        if 'user' in host:
            cfg['username'] = host['user']
        if 'IdentityFile' in host:
            cfg['key_filename'] = host['IdentityFile']
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(**cfg)

    def close(self):
        self.ssh.close()

    def run(self, func, *args, **kwargs):

        si, so, sr = self.ssh.exec_command('mktemp')
        tmpfile = so.read().rstrip().decode('utf-8')
        code = '\n'.join([
            inspect.getsource(func),
            inspect.getsource(_wrapper_function).format(
                func.__name__,
                repr(pickle.dumps(args)),
                repr(pickle.dumps(kwargs)),
                repr(tmpfile),
            ),
            "_wrapper_function()"
        ])
        if sys.version_info[0] == 2:
            si, so, sr = self.ssh.exec_command('python')
        else:
            si, so, sr = self.ssh.exec_command('python3')
        si.write(code)
        si.channel.shutdown_write()
        sys.stdout.write(so.read().decode('utf-8'))
        sys.stderr.write(sr.read().decode('utf-8'))
        si, so, sr = self.ssh.exec_command('cat {0};rm {0}'.format(tmpfile))
        ret = pickle.loads(so.read())
        if isinstance(ret, Exception):
            raise ret
        return ret
        return None


def _wrapper_function():
    import sys
    import os
    import pickle
    args = pickle.loads({1})
    kwargs = pickle.loads({2})
    tmpfile = {3}
    try:
        ret = {0}(*args, **kwargs)
    except Exception as e:
        ret = e
    with open(tmpfile, "wb") as f:
        pickle.dump(ret, f)
