from rempy import Remote

h = Remote('localhost')

def getfiles(dir='/'):
    return open("/home/eseifert/.ssh/id_rsa.pub").read()

ret = h.run(getfiles)

print ret
