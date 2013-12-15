from math import sqrt
import random

__author__ = 'Roland'


def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def euclid(a, b):
    if a == 0:
        return b
    if b == 0:
        return a

    while a > 0:
        a, b = b % a, a
    return b


def prime(n, k=10):
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = x * x % n
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True


def trial_div(n):
    remainder = 1
    if n % 2 == 0:
        remainder = 2
        yield 2
    for i in range(3, int(sqrt(n)) + 1, 2):
        if n % i == 0:
            yield i
    yield n // remainder


def generate_large_prime(nr=5):
    while True:
        p = random.randrange(10 ** nr, 10 ** (2*nr))
        if prime(p):
            return p


def get_generator(n):
    phi = n - 1
    factors = set(trial_div(phi))
    while True:
        a = random.randrange(2, n)
        if all(pow(a, phi // x, n) != 1 for x in factors):
            return a


def generare_cheie():
    p = generate_large_prime(1)
    g = get_generator(p)
    a = random.randint(2, p - 2)
    return (p, g, pow(g, a, p)), a


def encrypt(public_key, m):
    p, g, h = public_key
    k = random.randint(1, p - 2)
    while euclid(k, p - 1) != 1:
        k = random.randint(1, p - 2)
    gamma = pow(g, k, p)
    delta = m * pow(h, k, p) % p
    return gamma, delta


def decrypt(public_key, private_key, gamma, delta):
    return modinv(pow(gamma, private_key, public_key[0]), public_key[0]) * delta % public_key[0]

if __name__ == '__main__':
    pub, priv = generare_cheie()
    print(pub)
    cyp = encrypt(pub, 3698)
    print(decrypt(pub, priv, *cyp))
    print(euclid(150, 45))
    print(extended_gcd(150, 45))