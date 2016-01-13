from telepythy import Remote

def do_remote_thing(dir='/'):
    import os
    print "I am remote!"
    return os.listdir(dir)

server = 'localhost'

s = Remote(server)
try:
    dir_list = s.run(
        do_remote_thing,
        dir="/usr"
    )
except Exception as e:
    print 'I even handle remote exceptions! %s'%e

for dir in dir_list:
    print(dir)
