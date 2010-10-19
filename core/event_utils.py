'''
Created on Oct 12, 2010

@author: EB020653

@status: DEPRECATED!?
'''

class EVENT_NOT_SET():
    pass

class EVENT_NOT_CALLABLE():
    pass

class EVENT_CALLED():
    pass

def check_and_fire_event(event, *args, **kwargs):
    """
        Check if event is callable, is so, call it with the args.
        If not return an accoding value
    """
    if event is not None:
        if callable(event):
            result = event(args, kwargs)
            if result is None:
                return EVENT_CALLED
        else:
            return EVENT_NOT_CALLABLE
    else:
        return EVENT_NOT_SET
    return result
