'''
Created on Oct 12, 2010

@author: EB020653
'''
import unittest
from event_utils import *

def event_return_true(*args, **kwargs):
    return True

def event_cb_for_test(*args, **kwargs):
    pass

class Test_Event_Utils(unittest.TestCase):

    event_unset = None
    event_bad_setted = 1
    event_got_true = event_return_true
    event_got_none = event_cb_for_test
    
    
    def test_event_firing(self):
        event_result = check_and_fire_event(self.event_unset, dummyparam=1)
        self.assertEqual(event_result, EVENT_NOT_SET)
        event_result = check_and_fire_event(self.event_bad_setted, dummyparam=1)
        self.assertEqual(event_result, EVENT_NOT_CALLABLE)
        event_result = check_and_fire_event(self.event_got_true, dummyparam=1)
        self.assertTrue(event_result)
        event_result = check_and_fire_event(self.event_got_none, dummyparam=1)
        self.assertEqual(event_result, None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
