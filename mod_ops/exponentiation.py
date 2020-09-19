from time import time

def exp_mod(a, b, n):
    f = 1
    b = "{0:b}".format(b)
    k = len(b)
    for i in range(0, k):
        f = (f*f) % n
        if b[i] == '1':
            f = (f*a) % n
    return f


def exp_modr(a, b, n):
    if b == 1:
        return a % n 
    a2 = a*a % n
    if b % 2 == 0:
        return exp_mod(a2, b//2, n)
    else:
        a = a*a2 % n
        return exp_mod(a, b-1//2, n)
