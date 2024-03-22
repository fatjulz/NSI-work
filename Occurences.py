def occurrences(caractere, chaine):
    count = 0
    for char in chaine:
        if char == caractere:
            count += 1
    return count

occurrences('e', "sciences")
occurrences('i',"mississippi")
occurrences('a',"mississippi")
