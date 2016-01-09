from telepythy import Remote

h = Remote('localhost')


def getfiles(dir='/'):
    return open("/etc/hosts").read()


try:
    print h.run(getfiles, dir="/home")
    h.close()
except Exception as e:
    print "Handled Exception..."
    print e
