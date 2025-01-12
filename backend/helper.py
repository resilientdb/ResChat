from datetime import datetime
import inspect
from fileinput import filename


def combine_string_in_ascii(str1: str, str2: str) -> str:
    """
    Sort two strings in ASCII chat order
    """
    if str1 < str2:
        return str1 + str2
    else:
        return str2 + str1



def write_log(message: str):
    with open("log.txt", "a") as log:
        caller_file = inspect.stack()[1].filename
        caller_function = inspect.stack()[1].function
        caller_line = inspect.stack()[1].lineno
        log_message = f"[{str(datetime.now())}]\t\tFile: {caller_file}\t\tFunction: {caller_function}\t\tLine: {caller_line}\t\tMessage: {message}\n"
        log.write(log_message)
        log.close()
    return