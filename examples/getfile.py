from telepythy import Remote

h = Remote('localhost')


def getfile(filename="/etc/hosts"):
    return open(filename).read()


try:
    print h.run(getfile)
    h.close()
except Exception as e:
    print "Handled Exception..."
    print e
