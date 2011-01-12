'''
Created on Dec 12, 2010

@author: EB020653
'''
from core import core
from time import sleep
import sys

APPEXIT_REQUEST_EVENT_HASH = ""


def request_to_exit(*args, **kwargs):
    print "Saliendo"
    sys.stdout.write("Pero antes esperemos un poco")
    for i in xrange(5):
        sys.stdout.write(".")
        sleep (1)
    print "Listo!"
    return
    

if __name__ == "__main__":
    APPEXIT_REQUEST_EVENT_HASH = core.new_event("main", "exit")
    core.register_to_event("main", "exit", request_to_exit) 
    t = 0
    while True:
        t += 1
        if t > 1000:
            core.fire_event(APPEXIT_REQUEST_EVENT_HASH)
            break
            
   
    print "Terminado"
