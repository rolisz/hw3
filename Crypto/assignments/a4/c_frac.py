from collections import Counter

__author__ = 'Roland'


def trial_division_primes(n):
    divizori = Counter()
    if n < 0:
        divizori[-1] = 1
        n = abs(n)
    sqrt_n = int(abs(n)**0.5)

    i = 2
    if n % i == 0:
        divizori[i] +=1
        rest = trial_division_primes(int(n/i))
        divizori.update(rest)
        return divizori
    i = 3

    while i <= sqrt_n:
        if n % i == 0:
            divizori[i] +=1
            rest = trial_division_primes(int(n/i))
            divizori.update(rest)
            return divizori
        i += 2

    if n > 1:
        divizori[n] += 1
    return divizori

n = int(input())
print(trial_division_primes(n))
i = 0

a = [int(n ** 0.5)]
b = [int(n ** 0.5)]
bsq = [b[0] ** 2 - n]
x = [n ** 0.5 - a[0]]
primes = [trial_division_primes(bsq[0])]
for i in range(1, 10):
    a.append(int(1 / x[i - 1]))
    x.append(1 / x[i - 1] - a[i])
    if i > 1:
        b.append((a[i] * b[i - 1] + b[i - 2]) % n)
    else:
        b.append((a[i] * b[i - 1] + 1) % n)
    if b[i]**2 % n > n /2:
        bsq.append(b[i] ** 2 % n - n)
    else:
        bsq.append(b[i] ** 2 % n)
    primes.append(trial_division_primes(bsq[i]))


for i in range(1, 10):
    print(i, a[i], b[i], bsq[i], primes[i])
#print(a)
#print(b)
#print(x)
#print(bsq)
#print(primes)