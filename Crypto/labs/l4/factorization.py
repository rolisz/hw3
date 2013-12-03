from functools import reduce
from math import sqrt, log
from random import randint, getrandbits
from matplotlib import pyplot as plt
from time import time

__author__ = 'Roland'


def product(l):
    rez = 1
    for a in l:
        rez *= a
    return rez


def lcm(l):
    return product(l) // reduce(gcd, l, max(l))


def gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    while a > 0:
        temp = a
        a = b % a
        b = temp
    return b

def trial_div(n):
    if n % 2 == 0:
        return 2
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            return i
    return n

def factor(n, method=trial_div, B=None):
    divisors = []
    orig = n
    while n != 1:
        if method == pollard_p1 and B is not None:
            div = method(n, B)
            B += 2
        else:
            div = method(n)
        divisors.append(div)
        n //= div
    return divisors


def pollard_p1(n, B = None):
    if n < 150:
        return n
    if B is None:
        B = randint(5, int(log(n)))
    k = lcm(range(1, B))
    a = randint(2, n - 2)
    a = pow(a, k, n)
    d = gcd(a - 1, n)
    if d not in (1, n):
        return d
    return n

def test(a):
    t = time()
    print(factor(a))
    t1 = time() - t
    t = time()
    print(factor(a, pollard_p1))
    return t1, time() - t

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'graph':
        time_trial = []
        time_pollard = []
        nrs = []
        r = 60
        for i in range(20):
            nrs.append(getrandbits(r))
        nrs.sort()
        for nr in nrs:
            print(nr)
            rez = test(nr)
            time_trial.append(rez[0])
            time_pollard.append(rez[1])
        print(time_pollard)
        print(time_trial)
        plt.plot(nrs, time_trial)
        plt.plot(nrs, time_pollard)
        plt.xlim([2**(r - 10), 2**r])
        plt.ylim([0, 5])
        plt.show()
    else:
        x, b = input("Give an integer to factorize and the bound for Pollards p-1 method").split()
        print("Trial division: ")
        print(factor(int(x)))
        print("P-1:")
        print(factor(int(x), pollard_p1, int(b)))
