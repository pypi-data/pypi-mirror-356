import json
import sys
import traceback

from dtiot_d2c.d2c import utils as utils
from dtiot_d2c.d2c.utils import color as color

# Log levels
DEBUG = 10
INFO = 20
WARNING=30
ERROR = 40
CRITICAL = 50

def print_ERROR(s:str, **kwargs):
    print(f"{color.RED}{s}{color.END}", **kwargs)
    
def print_OK(s:str = "OK", **kwargs):
    print(f"{color.GREEN}{s}{color.END}", **kwargs)

def print_BOLD(s:str, **kwargs):
    print(f"{color.BOLD}{s}{color.END}", **kwargs)       
    
def load_test_configuration(run_id:str, config_file:str, config_var:str)->dict:
    ### Load configuration
    cfg_mod = utils.importModule("test_configuration", config_file)
    cfg = getattr(cfg_mod, config_var)

    # Replace some config variables
    s = json.dumps(cfg)
    for (var_name, var_value) in [["%RUNID%", run_id]]:
        s = s.replace(var_name, var_value)
    cfg = json.loads(s)
    
    #for (k, v) in cfg.items():
    #    if cfg[k] and type(cfg[k]) == str:
    #        cfg[k] = cfg[k].replace("%RUNID%", run_id)    
            
    return cfg            

def call_has_element_value(d:dict, elem_path:str, test_value):
    b = utils.has_element_value(d, elem_path, test_value)
    #ok = "OK" if b else "NOT OK"
    #print(f"{ok}: has_element_value(node_response, {elem_path}, {test_value})")  
    return b  

def exec_test(label:str, test_func, *args, **kwargs):
    try:
        print(f"{label} ... ", end="", flush=True)
        rv = test_func(*args, **kwargs)
        print_OK(flush=True)
        return rv
    except Exception as ex:
        print_ERROR(f"ERROR: {ex}", flush=True)
        traceback.print_exc()
        return str(ex)