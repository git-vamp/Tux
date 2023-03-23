from xdg.BaseDirectory import xdg_data_dirs
from pathlib import PosixPath
import os
from typing import List
from logger import logger

def extract_data():
    app_path = lambda path : PosixPath(path + '/applications')
    data_array: List[str] = []
    for dir in xdg_data_dirs:
        dir_path = lambda path : PosixPath(f"{dir}/applications/{path}")
        if not app_path(dir).exists(): continue
        files = os.listdir(dir)
        if  len(files) == 0: continue 
        data_array.extend(
                [str(dir_path(file)) for file in os.listdir(app_path(dir))]
        )
   
    return data_array



def parse_ext(name:str="") -> str:
    data = [ext for ext in extract_data() if ext.endswith('.desktop') and name in ext]
    if len(data) == 0: return "App Not Found"
    else: 
        os.system(f"dex {data[0]}")
        return f"Launching {PosixPath(data[0]).name.replace('.desktop', '')}"
