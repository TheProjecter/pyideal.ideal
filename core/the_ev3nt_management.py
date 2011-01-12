'''
Created on Oct 13, 2010

@author: EB020653
'''
import settings
from hashlib import md5
import types
import logging


class Event_Stop_Processing():
    def __init__(self):
        raise NotImplementedError("NEVER try to instance me!")

EVENT_STOP_PROCESSING = Event_Stop_Processing

class Ev3ntManager(object):
    __events_funcs = None
    __events_id = None
    __events_auth = None
    
    def __init__(self):
        self.__events_funcs = dict()
        self.__events_id = dict()
        self.__events_auth = dict()
    
    def new_event(self, event_name, event_permission_cb=None):
        if event_name == "":
            raise ValueError("""You need to specify a name for the event!""")
        event_hash = md5(event_name).hexdigest()
        self.__events_id.update({event_name : event_hash})
        self.__events_funcs.update({self.__events_id[event_name] : Ev3nt()})
        if event_permission_cb is not None:
            self.__events_auth.update({self.__events_id[event_name] : event_permission_cb})
        return event_hash
    
    def register_to_event(self, event_name, event_handler):
        if event_name == "":
            raise ValueError("""You need to specify a name for the event!""")
        self.__events_funcs[self.__events_id[event_name]] += event_handler
    
    def unregister_to_event(self, event_name, event_handler):
        if event_name == "":
            raise ValueError("""You need to specify a name for the event!""")
        self.__events_funcs[self.__events_id[event_name]] -= event_handler
    
    def fire_event(self, event_hash, *args, **kwargs):
        if event_hash == "":
            raise ValueError("""You need to specify a name for the event!""")
        self.__events_funcs[event_hash](args, kwargs)

    def get_event_hash (self, event_name, event_token):
        if event_name == "":
            raise ValueError("""You need to specify a name for the event!""")
        if event_token == "":
            raise ValueError("""You need to give a token for the authorization!""")
        try:
            if self.__events_auth[event_name](event_token):
                return self.__events_id[event_name]
        except KeyError:
            raise ValueError ("""We don't have registered an auth manager for this event""")
        finally:
            return None

class Ev3nt(object):
    __handlers = None
    def __init__(self):
        self.__handlers = list()
        if settings.EVENT_DEBUGGING:
            #import logging
            fn = settings.EVENT_LOG
            if fn == "" or fn is None:
                fn = ".\event-log.log"
                logging.basicConfig(filename=fn, level=logging.DEBUG)

    def handle(self, handler):
        first = None
        func = None
        if handler is None:
            if settings.EVENT_DEBUGGING:
                logging.debug("""\
                On AddHandler - raise ValueError("
                How can i fire the event if this is 
                not a callable object?, come on! RTFM!")""")
            raise ValueError("Handler can't be None!, come on! RTFM!.")
        if isinstance(handler, types.TupleType): #split!
            first = handler[0]
            func = handler[1]
            if settings.EVENT_DEBUGGING:
                logging.debug("""Get a Tuple as handler, splitting!""")
        else:
            func = handler
        if not callable(func):
            if settings.EVENT_DEBUGGING:
                logging.debug("""\
                On AddHandler - raise ValueError("
                How can i fire the event if this
                 is not a callable object?, come on! RTFM!")""")
            raise ValueError("""\
            How can i fire the event if 
            this is not a callable object?, come on! RTFM!""")
        if settings.EVENT_DEBUGGING:
            logging.debug("Start AddHandler:{0}".format(func.__name__))
        if first is None:
            mode = "normal"
            self.__handlers.insert(len(self.__handlers) / 2, handler)
        else:
            if first:
                mode = "At start"
                self.__handlers.insert(0, handler)
            else:
                mode = "At end"
                self.__handlers.append(handler)            
        if settings.EVENT_DEBUGGING:
            logging.debug("End AddHandler:{0}-mode:{1}".format(handler.__name__, mode))
        return self

    def unhandle(self, handler):
        try:
            if isinstance(handler, str):
                for one_handler in self.__handlers:
                    if one_handler.__name__ == handler:
                        self.__handlers.remove(one_handler)
                        break
            else:
                self.__handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.__handlers:
            if settings.EVENT_DEBUGGING:
                logging.debug("""Calling: {0}""".format(handler.__name__))
            retval = handler(*args, **kargs)
            if retval == EVENT_STOP_PROCESSING:
                if settings.EVENT_DEBUGGING:
                    logging.debug("""EVENT_STOP_PROCESSING from:{0}""".format(handler.__name__))
                return          

    def get_handler_count(self):
        return len(self.__handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__ = get_handler_count




def test_reg(event_manager):
    
    def eventhandler(*args, **kwargs):
        print "event!"
    
    eventIds = set()
    for i in xrange(10):
        eventname = "event_" + str(i)
        eventIds.add(event_manager.new_event(eventname))
        #event_manager.register_to_event(eventname, eventhandler)
        for k in xrange(10):
            event_manager.register_to_event(eventname, eventhandler)
    return eventIds

def test_fire(event_manager, eventIds):
    for h in eventIds:
        #eventname="event_"+str(i)
        event_manager.fire(h)
    return
    
if __name__ == "__main__":
    from timeit import Timer
    print "Testing speed, this take a while! (a million repetition for each!):"
    print "Generating 10 events and register 10 events handler for each event."
    #test_reg()
    t = Timer("evtmng=test_reg(event_manager);", "from __main__ import test_reg, Ev3ntManager; event_manager=Ev3ntManager();")
    k = 1000000
    event_reg_results = k * t.timeit(number=k) / k
    print "Done!"
    print "Firing up all events!, console madnessssssssssss!."
    t = Timer("test_fire(evtmng)", "from __main__ import test_reg, Ev3ntManager; event_manager=Ev3ntManager(); evtmng=test_reg(event_manager);")
    event_fire_results = k * t.timeit(number=k) / k
    print "Done!"
    print "So, lately there is the stats:"
    print "Register 10 events and 10 handlers %.2f usec/pass" % event_reg_results
    print "Firing up all events: %.2f usec/pass" % event_fire_results
    print "Thats All Folks!."
            
            
            
            
