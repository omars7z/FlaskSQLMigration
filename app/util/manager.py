import os
import importlib
from app.repositries.base_repositry import BaseRepositry
import inspect

def load_repositries():
    repo_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "repositries") #/app/repositries
    repositries = {}
    
    for filename in os.listdir(repo_dir):
        if not filename.endswith("_repositry.py"):
            continue
        
        module_name = f"app.repositries.{filename[:-3]}" #remove py
        module = importlib.import_module(module_name)
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseRepositry) and obj is not BaseRepositry:
                keys = name.replace("Repositry", "")
                repositries[keys] = obj()
                
        
    print("Loaded repositories:", list(repositries.keys()))            
    return repositries