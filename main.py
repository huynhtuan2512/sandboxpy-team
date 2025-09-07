import json
from src.sandbox_core import san_code_wwarning, runcode_safe

code_imput = """
import os
from os import system,path
print("Hello tuan dep trai")
os.getattr()
x = eval("2+2")
"""

warning_information = san_code_wwarning(code_imput)

result  = {
    "ok" : len(warning_information) == 0,
    "Warning" : warning_information
}
print(json.dumps(result, indent=2))

if warning_information:
    print("=====> Code nguy hiem nen khong the chay")
else :
    runcode_safe(code_imput)
