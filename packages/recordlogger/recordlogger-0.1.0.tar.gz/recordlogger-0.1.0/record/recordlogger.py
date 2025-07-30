import inspect
import os
import datetime

def get_type(value):
    obj_type = type(value)
    module = obj_type.__module__
    name = obj_type.__name__
    if module in ('builtins', '__main__'):
        return name
    else:
        return f"{module}.{name}"

def record(name, value, original_line, original_file, function_name, collection):
    if original_line is None or original_file is None:
        frame = inspect.stack()[1]
        lineno = frame.lineno
        filename = os.path.basename(frame.filename)
    else:
        lineno = original_line
        filename = original_file
    value_type = get_type(value)
    log_entry = {
        "name": name,
        "type": value_type,
        "value": str(value),
        "line": lineno,
        "file": f'{filename}',
        "function": function_name
        # "timestamp": datetime.datetime.now()
    }
    collection.update_one(
        {
            "name": name,
            "line": lineno,
            "file": filename,
            "function": function_name
        },
        {"$set": log_entry},
        upsert=True
    )
