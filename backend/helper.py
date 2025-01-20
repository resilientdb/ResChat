from datetime import datetime
import inspect
from fileinput import filename
import os
from textwrap import indent


def combine_string_in_ascii(str1: str, str2: str) -> str:
    """
    Sort two strings in ASCII chat order
    """
    if str1 < str2:
        return str1 + str2
    else:
        return str2 + str1



def write_log(message: str or Exception):
    time = datetime.now()
    caller_stack = inspect.stack()
    log_list = []
    for caller in reversed(caller_stack):
        log_list.append(f"{os.path.basename(caller.filename)} - {caller.function} - line {caller.lineno}")
    log_message = (
        f"[{str(time)}]\t"
        f"{log_list[0]}"
    )
    line_indent = "\t\t\t\t\t\t\t\t"
    for log in log_list[1:len(log_list)-1]:
        log_message += f"\n{line_indent}└──>{log}"
        line_indent += "\t"
    log_type = "Message" if isinstance(message, str) else "Error"
    log_message += f"\t\t{log_type}: {message}\n\n"
    with open("log.txt", "a") as log:
        log.write(log_message)
        log.close()
    return


def clear_cache():
    temp_path = "temp/"
    if not os.path.exists(temp_path):
        print(f"文件夹 {temp_path} 不存在。")
        return

    # 遍历文件夹中的所有文件
    for filename in os.listdir(temp_path):
        file_path = os.path.join(temp_path, filename)
        os.remove(file_path)

    return
clear_cache()
