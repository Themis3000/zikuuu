def array_to_readable(array):
    string = ""
    for i in range(len(array)-1):
        string = string + str(array[i]) + ", "
    string = string + str(array[len(array)-1])
    return string
