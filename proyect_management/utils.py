'''
Created on Oct 11, 2010

@author: EB020653
'''
from hashlib import sha1


def hash_data(data):
    return sha1(data).hexdigest()

def get_hash_for(filename):
    f = open(filename, "rb")
    fc = f.read()
    f.close()
    return hash_data(fc)

#quick-and-dirty enum type :)
def enum(*seq_args, **named_args):
    enum = dict(zip([x.upper() for x in seq_args], range(len(seq_args))))
    enum.update([(k.upper(), v) for [k, v] in named_args.iteritems()])
    #No bases, object as base make this: http://is.gd/fYbvs
    return type('qdEnum', (), enum)

    
