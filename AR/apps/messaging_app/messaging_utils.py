def space_split(string : str, cutoff : int):
    string = string.strip().split(" ")

    if len(string) == 1:
        return string[0]

    display_string = ""
    temp_string = ""
    for i in string:
        if len(temp_string + i) + 1 > cutoff:
            display_string += temp_string + "\n"
            temp_string = ""

        temp_string += " " + i

    return display_string