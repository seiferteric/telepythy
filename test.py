from rempy import Remote

h = Remote('localhost')


def getfiles(dir='/'):
    return open("/etc/hosts").read()


try:
    print h.run(getfiles, dir="/home")
except:
    print "Handled Exception..."
