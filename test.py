from rempy import Remote

h = Remote('localhost')

def getfiles(dir='/'):
    return open("/myfile").read()


try:
    print h.run(getfiles)
except:
    print "Handled Exception..."

