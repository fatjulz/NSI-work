"""Question 1"""

#1.a
def is_palindrome(x):
    """Reads an integer x and returns True if x is a palindrome and False otherwise"""
    x_str = str(x)
    return x_str == x_str[::-1]

def palindromic_sums(n):
    """Reads an integer n between 1 and 1000000 inclusive and ouputs 1, 2 or 3 palindromic
      numbers which together form a minimal length palindromic sum for the input n"""

    if n < 1 or n > 1000000:
        return "Invalid input"

    if is_palindrome(n):
        return [n]
    for i in range(1, n):
        if is_palindrome(i) and is_palindrome(n - i):
            return [i, n - i]


    for i in range (1, n):
        for j in range (1, n):
                if is_palindrome(i) and is_palindrome(j) and is_palindrome(n - i - j):
                    return [i, j, n - i - j]
    

#1.b
assert palindromic_sums(54) == [1, 9, 44]

#1.c



