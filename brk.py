# function that breaks a string into a array of strings no much longer of 70 characters
# if the string is not longer than 70 characters, it returns an array of just one element
# if it's longer it splits taking into account the first space after the character 70
# to split the string and so on.
def breakline(line: str):
    lines = []
    right = line
    while True:
        pos = right.find(" ",67)
        if pos != -1:
            left = right[:pos]
            right = right[pos+1:]
        else:
            left = right
        lines.append(left)
        if left == right:
            break
    return lines