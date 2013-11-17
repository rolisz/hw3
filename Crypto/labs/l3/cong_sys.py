__author__ = 'Roland'
import operator

def modular_inverse(x, n=27):
    for i in range(n):
        if x*i % n == 1:
            return i


def gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    while a > 0:
        temp = a
        a = b%a
        b = temp
    return b

def solve_system(a_list, n_list):
    if any(gcd(a,b) != 1 for a in n_list for b in n_list if a != b):
        return "n-urile nu sunt prime intre ele"
    N = reduce(operator.mul, n_list, 1)
    x = 0
    for a, n in zip(a_list, n_list):
        K = modular_inverse(N/n, n)
        x += a* N/n * K % N
    return x % N

a_list = []
n_list = []
inp = True
print("Dati ecuatiile sub forma a_i n_i")
while inp:
    inp = raw_input()
    if inp:
        a, n = inp.split()
    else:
        break
    a_list.append(int(a))
    n_list.append(int(n))


print("Solutia este: ")
print(solve_system(a_list, n_list))

