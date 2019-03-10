import datetime

def array_to_comma_list(array):
    string = ""
    for i in range(len(array)-1):
        string = string + str(array[i]) + ", "
    string = string + str(array[len(array)-1])
    return string


def array_to_space_list(array):
    string = ""
    for i in range(len(array)-1):
        string = string + str(array[i]) + " "
    string = string + str(array[len(array)-1])
    return string


def seconds_to_readable(seconds):
    return datetime.timedelta(seconds=seconds)
