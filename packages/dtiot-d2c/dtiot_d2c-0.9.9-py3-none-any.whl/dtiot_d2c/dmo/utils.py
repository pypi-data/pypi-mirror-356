import importlib
import json
import logging
import os
import os.path
import sys
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def splitString(str, sepChar):
    a = []
    for s in str.split(sepChar):
        a.append(s.strip())
    return a

def isDict(obj):
    if not obj:
        return False
    else:
        return True if obj.__class__ == {}.__class__ else False

def isArray(obj):
    if not obj:
        return False
    else:
        return True if obj.__class__ == [].__class__ else False

def isString(obj):
    return obj.__class__ == "str".__class__ if obj else False

def convert_str_to_python_type(s:str):
    if not s:
        return s
    
    try:
        return int(s)
    except Exception:
        pass
    
    try:
        return float(s)
    except Exception:
        pass
    
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False

    try:
        result = json.loads(s)
        if isinstance(result, (list, dict, tuple)):
            return result
    except json.JSONDecodeError:
        pass            
    
    return s

from enum import Enum


class ReturnType(Enum):
    TEXT = 1
    JSON_AS_DICT = 2
    LINES_AS_LIST = 3

def execCmd(cmd, returnType : ReturnType = ReturnType.TEXT):
    log.debug("Exec %s" % (cmd))
        
    cmdIn = os.popen(cmd)

    line = cmdIn.readline()
    s = ""
    while line:
        if line.startswith("b\'"):
            line = line.strip()
            line = line[2:-1] + "\n"
        s = s + line
        line = cmdIn.readline()    

    log.debug("\n%s" % (s.strip()))                                  

    if returnType == ReturnType.JSON_AS_DICT:
        return json.loads(s)
    elif returnType == ReturnType.LINES_AS_LIST:
        return splitString(s, "\n")
    else:
        return s
    
class FileLinesIterator:
    '''
    Iterator class to walk through lines of a text file in the context of for loop.

    Sample code:    

    from file_lines_iter import FileLines

    for line in FileLinesIterator("/Users/rolan/Desktop/WORK/1646599091.json"):
        print(line)
        
    '''
    
    def __init__(self, filepath, stripLines:bool=False, skipEmptyLines:bool=False, skipLinesStartWith:list[str]=[]):
        '''
        Constructor of FileLinesIterator class.
        :param filepath: Path of the file through which lines shall be iterated. If "-" than stdin is read
        :param skipLines: If set all lines are left and right stripped.
        :param skipEmptyLines: If set to true empty lines are not returned.
        :param skipLinesStartWith: Array of single characters. If a line starts with one of the chars it is not returned.
        '''
        self._filepath = filepath
        self._file = None
        self._skipEmptyLines=skipEmptyLines
        self._skipLinesStartWith=skipLinesStartWith
        self._stripLines=stripLines

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self._file:
            if self._filepath=="-":
                self._file = sys.stdin
            else:
                self._file = open(self._filepath, "r")

        while True:
            line = self._file.readline()
            if not line:
                if self._filepath!="-":
                    self._file.close()
                raise StopIteration

            if self._stripLines:
                line=line.strip()
            else:
                line=line.rstrip()
                
            if self._skipEmptyLines and len(line)==0:
                continue

            if len(line)>0 and line[0] in self._skipLinesStartWith:
                continue

            return line

import socket


def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# Class to executues a function every x seconds 
import threading
import time
import traceback


class FunctionExecutor(threading.Thread):
    def __init__(self, cronSecs, function, *args, **kwargs):
        super().__init__()
        self._cronSecs = cronSecs
        self._function = function
        self._args = args
        self._kwargs = kwargs

    def run(self):
        while True:
            try:
                time.sleep(self._cronSecs)
                self._function(*self._args, **self._kwargs)
            except Exception as ex:
                log.error(str(ex))
                traceback.print_exc()
                
def getValueFromDict(rootD:dict, elemPath:str, default:any=None, sepChar=".") -> any:
    '''
    Gets a value from a dictionary element.
    '''
    d = rootD
    names = elemPath.split(sepChar)
    name = names[0]    

    if name not in d.keys() or len(names) == 0:
        return default
    elif len(names) == 1:
        return d.get(name)            
    else:
        return getValueFromDict(d.get(names[0]), sepChar.join(names[1:]), default=default, sepChar=sepChar)

def hasElementInDict(rootD:dict, elemPath:str, sepChar=".") -> bool:
    '''
    Verifies if a specific element in the dictionary exists.
    Returns True if the element exists. 
    Return False if the element not exists.
    '''
    d = rootD
    names = elemPath.split(sepChar)
    firstName = names[0]    

    if firstName not in d.keys() or len(names) == 0:
        return False
    elif firstName not in d.keys():
        return False
    elif len(names) == 1:
        return True if firstName in d.keys() else False          
    else:
        return hasElementInDict(d.get(names[0]), sepChar.join(names[1:]), sepChar=sepChar)

def setValueInDict(rootD:dict, elemPath:str, value:any, sepChar=".", createIfNotExist=False) -> bool:
    '''
    Sets a value to an element in a dictionary.
    Returns True if the value of the element has been set.
    Return False if the value hasn't been set because the element does not exist.
    '''
    d = rootD
    names = elemPath.split(sepChar)
    firstName = names[0]    

    if firstName not in d.keys():
        if createIfNotExist:
            if len(names) > 1:
                for i in range(0, len(names) - 1):
                    d[names[i]] = {}
                    d = d[names[i]]
            d[names[-1]] = value
            return True
        else:
            return False

    # At this point the element with firstName always exist.
    # If we reached the leaf of the path
    if len(names) == 1:
        d[firstName] = value
        return True
    else:
        return setValueInDict(d.get(names[0]), sepChar.join(names[1:]), value, sepChar=sepChar, createIfNotExist=createIfNotExist)

def flattenDict(inD:dict, prefix:str="", sepChar:str="_")->dict:
    '''
    Walks top/down through a multi-level dictionary and creates out of it a dictionary
    with only a single level. The names of the sub-dictionary in the input dictionary
    are separated in the name of the return dictionary by a separator character.
    
    :param inD:dict:     Mulit level input dictionary which shall be converted into a single level dictionary.
    :param prefix:str:   Name prefix which shall be used.
    :sepChar:str:        Seperator character.A
    
    :return:dict:       Single level dictionary
    '''
    retD = {}
    for k in inD.keys():
        e = inD[k]
        if type(e) == dict:
            d = flattenDict(e, prefix=f"{prefix}{k}{sepChar}", sepChar=sepChar)
            retD.update(d)
        else:
            retD[f"{prefix}{k}"] = inD[k]

    return retD

def get_value_from_dict_3(rootD:dict, elemPath:str, default:any=None, sepChar=".") -> any:
    # If rootD is not a dictionary but a list, call this function for each element 
    # of the list
    if type(rootD) in [list, tuple]:
        values = []
        for e in rootD:
            v = get_value_from_dict_3(e, elemPath, default=default, sepChar=sepChar)
            values.append(v)
        return values
    elif type(rootD) != dict:
        return ""
    
    d = rootD
    names = elemPath.split(sepChar)
    name = names[0]    

    # If name represents an elemement in an array such as dvi[0]
    list_idx = -1
    
    if (idx1 := name.find("[")) > -1:
        if (idx2 := name.find("]", idx1)) == -1:
            return default
        list_idx = int(name[idx1+1:idx2])
        name = name[0:idx1]
        
    if name not in d.keys() or len(names) == 0:
        return default
    elif len(names) == 1:
        if list_idx == -1:
            return d.get(name)            
        else:
            l = d.get(name)
            return l[list_idx] if list_idx < len(l) else default
    else:
        if list_idx == -1:
            return get_value_from_dict_3(d.get(names[0]), sepChar.join(names[1:]), default=default, sepChar=sepChar)
        else:
            l = d.get(name)
            if list_idx >= len(l):
                return default
            return get_value_from_dict_3(l[list_idx], sepChar.join(names[1:]), default=default, sepChar=sepChar)
    
def suppressEx(func, *args, **kwargs) -> any:
    '''
    Runs a function and suppresses an exception. 
    
    :param *args: Optional arguments to pass into the function.
    :param **kwargs: Option keyword arguments to pass into the function.
    
    :return: Return of the function or None in case an exception is caught.
    '''
    try:
        return func(*args, **kwargs)
    except Exception as ex:
        log.error(f"Error while exec {func.__name__}: {ex}")        
        return None           
    
########################################################################
#MARK: base64
########################################################################
import base64


def str_to_b64str(s:str)->str:
    if not s:
        return s
    b = s.encode('utf-8')
    b64 = base64.b64encode(b)
    return b64.decode('utf-8')    
    
def to_basic_auth(username:str, password:str)->str:
    return str_to_b64str(f"{username}:{password}")

###
# Some usefull decorators
#MARK: profile decorator
from functools import wraps


def profile(log_func=None,       # Logger function to use for output. 
                                 # If not defined "print" is used to output to stdout.
            log_prefix="profile" # Prefix string for the log output
):                               # Any value of decorated function
    '''
    Function decorator to print function call arguments and execution time to stdout or a logger.
    
    By default the profile decoration is switchd off. To switch it on export the environment 
    variable DTIOT_PROFILE=1.
    
    How to use the profile decorator:

    import utils

    @utils.profile(log_func=log.info)
    def myFunc(name):
        print(f"Hallo from {name}")
    '''
    
    if not log_func:
        log_func = print
        
    def decorator(fu):
        if os.getenv("DTIOT_PROFILE", "false").lower() not in ["1", "true", "yes"]:
            return fu
        @wraps(fu)
        def wrapper(*args, **kwargs):
            s = ""
            for a in args:
                if s:
                    s += ", "
                s += f"{a}" 
            for (k, v) in kwargs.items():
                if s:
                    s += ", "
                s += f"{k}={v}" 
            log_func(f"{log_prefix}: calling {fu.__name__}({s})")
                
            before = time.time()
            rv = fu(*args, **kwargs)
            after = time.time()
            
            log_func(f"{log_prefix}: called {fu.__name__}: {after - before:.6f} secs")

            return rv
        return wrapper
    return decorator   
    
########################################################################
#MARK: date function
########################################################################
from datetime import datetime


def fnow(format:str="%Y-%m-%d %H:%M:%S")->str:
    return datetime.now().strftime(format)

class DatetimeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super().default(obj)              
        
        