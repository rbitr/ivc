# vc.py
import hashlib
import inspect
from datetime import datetime
from difflib import Differ
import pandas as pd
from IPython.utils import capture
import matplotlib.pyplot as plt 
import sys
import functools

class VC:

    def __init__(self):
        self.versions = {}

    def get_dict(self):
        return self.versions 

    def get_entries(self):
        rv = {}
        for i in self.get_dict():
            dfr = pd.DataFrame(self.get_dict()[i]).T
            dfr.index=dfr.index.rename(i) 
            rv[i]=dfr    
        
        return rv  

    def func_hash(self,func):
        hashfunc = hashlib.md5
        return hashfunc(inspect.getsource(func).encode('utf-8')).hexdigest()


    def display(self,func,entry):
        if type(func)!=str:
            func=func.__name__
 
        e = self.versions[func][entry]
        if "last_output" in e:
            output = e["last_output"]
            
            if output[0] is not None:
                print(output[0])

            if output[1] is not None:
                print(output[1],file=sys.stderr)

            if output[2] is not None:
                for j in output[2]:
                    j.display()            

    def summary(self,func=None):
        summ={}
        if func is None:
            for func in self.versions:
                summ[func]=len(self.versions[func])
                
        else:
            if type(func)!=str:
                func=func.__name__
            for ha in self.versions[func]:
                summ[ha]=self.versions[func][ha]["count"]


        return summ
     

    def diff(self,func,entry1,entry2):
        d = Differ()
        if type(func)!=str:
            func=func.__name__
     
        s1 = self.versions[func][entry1]["source"].split('\n')
        s2 = self.versions[func][entry2]["source"].split('\n')
        return list(d.compare(s1,s2))
     

    def add_vc(self,comment="",capturing=True):
        def wrapper(func):
            # if not in the dictionary, add to the dictionary
            h = self.func_hash(func)
            if func.__name__ not in self.versions:
                self.versions[func.__name__]={}

            if  h not in self.versions[func.__name__]:
                self.versions[func.__name__][h]={"source":inspect.getsource(func), "timestamp":datetime.now().isoformat(), "comment":comment,"count":0}
            else:
                self.versions[func.__name__][h]["timestamp"]=datetime.now().isoformat()
                if comment != "": self.versions[func.__name__][h]["comment"]=comment


            
            # return a function that captures the output of func and
            # saves it somewhere
            @functools.wraps(func)
            def output_capture(*args,**kwargs):
                # is it better to cache when the function is defined or when it's run?
                with capture.capture_output() as cap:
                    retval = func(*args,**kwargs)
                
                # there should be an entry associated with the function's current hash. Find that and insert the output there... 
                # ideally, should check if the output hashes to what it did the last time, and if not create a new entry
                # non-ideal version:
                h = self.func_hash(func)    
                self.versions[func.__name__][h]["last_output"]=(cap.stdout,cap.stderr,cap.outputs)
                self.versions[func.__name__][h]["count"]+=1
                # display it
                try:
                    cap()
                except:
                    print("problem displaying output: "+func, file=sys.stderr)

                return retval

            if capturing: 
                return output_capture
            else:
                return func 

        return wrapper   
