import ast
from src.runner import Limit_resource 

Dangerous_module = [
    "os", "sys", "subprocess", "socket", "shutil", "pathlib",
    "temppfile", "glob", "fnmatch", "ftplib", "telnetlib",
    "http.client", "urllib", "pickle", "marshal", "dill",
    "ctypes", "cffi", "multiprocessing", "threading", "resource", "signal"
]
Dangerous_builtin = [
    "eval", "exec", "__import__", "open", "input", "compile",
    "globals", "locals", "exit", "quit", "getattr", "setattr",
    "delattr", "vars", "dir", "help","super","__subclasses__"
]

Safe_module = {
    "math" : __import__("math"),
    "random": __import__("random"),
    "itertools": __import__("itertools"),
    "functools": __import__("functools"),
    "operator": __import__("operator"), 
    "string": __import__("string"),
    "re": __import__("re"), 
    "collections": __import__("collections"),
    "heapq": __import__("heapq"),          
    "bisect": __import__("bisect"),         
    "array": __import__("array"),          
    "datetime": __import__("datetime"),    
    "time": __import__("time"),            
    "decimal": __import__("decimal"),      
    "fractions": __import__("fractions"),  
    "json": __import__("json"),   
}

Safe_builtin = {
    "print" : print,
    "float" : float,
    "str" : str,
    "range" : range,
    "zip" : zip,
    "tuple" : tuple,
    "abs" : abs,
    "max" : max,
    "min" : min,
    "list" : list,
    "len" : len,
    "dict" : dict,
    "bool" : bool,
    "complex" : complex,
    "format" : format,
    "hex" : hex,
    "isinstance" : isinstance,
    "set" : set,
    "pow" : pow,
    "bin" : bin
}

def san_code_wwarning(code):
    waring_information = []
    try :
        tree = ast.parse(code)
    except Exception as e:
        waring_information.append(f"Loi Exception: {e}")
        return waring_information
    
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            for asl in node.names:
                if asl.name in Dangerous_module:
                    waring_information.append(f"Loi khai bao Import nguy hiem : \"{asl.name}\" o dong thu {node.lineno}")
        if isinstance(node, ast.ImportFrom):
            if node.module in Dangerous_module:
                waring_information.append(f"Loi khai bao from tu Import nguy hiem : \"{node.module}\" o dong thu {node.lineno}")
        if isinstance(node,ast.Call):
            if isinstance(node.func, ast.Name):
                    if getattr(node.func,'id','') in Dangerous_builtin:
                        waring_information.append(f"Loi khai bao goi ham nguy hiem : \"{node.func.id}\" o dong thu {node.lineno}")
            elif isinstance(node.func, ast.Attribute):
                value_import = getattr(node.func.value, 'id','UNKNOWN')
                if node.func.attr in Dangerous_builtin:
                    if value_import in Dangerous_module:
                        waring_information.append(f"Loi khai bao ham nguy hiem : \"{node.func.attr}\" tu Import nguy hiem \"{value_import}\" o dong thu {node.lineno}")
                    else :
                        waring_information.append(f"Loi khai bao ham nguy hiem : \"{node.func.attr}\" o dong thu {node.lineno}")

    return waring_information


def runcode_safe(code):
    
    try:
        Limit_resource()
    except Exception as e:
        print("Loi gioi han tai nguyen : ", e)

    try:
        exec(code,{"__builtins__":Safe_builtin, **Safe_module})
    except Exception as e:
        print("Loi thuc thi code : ", e)