from functools import reduce
from random import randint 
from random import randrange, getrandbits
import DSA_pq
import random
import hashlib

N = 1024
L = 160

def extGCD(a, b):
    if b == 0:
        return 1, 0, a
    else:
        x, y, q = extGCD(b, a % b) # q = gcd(a, b) = gcd(b, a%b)
        x, y = y, (x - (a // b) * y)
        return x, y, q

def squreAndMultiply(plain, e, n):
    binary = bin(e)[2:]
    result = 1
    for i in binary:
        result = (result * result) % n
        if i == '1':
            result = (result * plain) % n
    return result

def miller_rabin(n, k=100):
    if n < 2:
        return False

    # d * 2 ^ s
    s = 0 
    d = n-1
    while d % 2 == 0:
        s += 1
        d /= 2
    

    # If 𝑥^2 ≡ 1 (mod 𝑝) for a prime 𝑝, then 𝑥 = ±1 (mod 𝑝)
    # If 𝑥 ≠ ±1 (mod 𝑁) but 𝑥^2 ≡ 1 (mod 𝑁) , then 𝑁 is a composite 
    for i in range(k):
        a = randrange(2, n - 1)
        b = squreAndMultiply(a,int(d),n) # a^d % n,產生亂數,試圖找到witness
        for j in range(s):
            if b != 1 and b != n-1:    #𝑥 ≠ ±1 (mod 𝑁)
                b = squreAndMultiply(b, 2, n)
                if b == 1: # 𝑥^2 ≡ 1 (mod 𝑁)
                    return False
    return True
    
def genPrime(n):
    p = random.randint(0,pow(2,n))
    while(miller_rabin(p) == False):
        p = random.randint(0,pow(2,n))
    return p


def genPrimePQ():
    q = genPrime(L)
    # p = genPrime(N)
    cnt = int(pow(2, 1024) / q)
    while(not miller_rabin(q * cnt + 1)):
        cnt -= 1
    p = q * cnt + 1
    return p, q

def genG(p, q):
    h = 2
    g = squreAndMultiply(h, int((p - 1) / q), p)
    while( squreAndMultiply(g , q , p) != 1):
        h += 1
        g = squreAndMultiply(h, int((p - 1) / q), p)
    return g

def genX(q):
    return random.randint(1, q)

def genY(g, x, p):
    return squreAndMultiply(g, x, p)

def genKR(p, q, g):
    k = random.randint(1, q)
    # k=15
    r = squreAndMultiply(g, k, p) % q
    while r == 0:
        k = random.randint(1, q)
        r = squreAndMultiply(g, k, p) % q
    return k, r

def H(m):
    sha1 = hashlib.sha1()
    sha1.update(m.encode("utf-8"))
    return(sha1.hexdigest())

def toPositive(n,r):
    while n<=0:
        n+=r
    return n

def genKey():
    # p = 303287
    # q = 151643  
    p, q = DSA_pq.gen_param()
    g = genG(p, q)
    x = genX(q)
    y = genY(g, x, p)
    return p, q, g, x, y

def sign(m, p, q, g, x):
    k, r = genKR(p, q, g)
    print(extGCD(k,q))
    inv = extGCD(q,k)[1]
    inv = toPositive(inv,q)
    h = int(H(m), 16)
    s = inv * (h + x * r)  % q
    while s == 0:
        k, r = genKR(p, q, g)
        inv = extGCD(q,k)[1]
        inv = toPositive(inv,q)
        h = int(H(m), 16) 
        s = inv * (h + x * r)  % q
    return r, s

def verify(m, r, s, p, q):
    if 0 < r and r < q or 0 < s and s < q:
        w = extGCD(q,s)[1]
        w = toPositive(w,q)
        u1 = (int(H(m), 16)  * w) % q
        u2 = (r * w) % q
        # v = (squreAndMultiply(g, u1 ,p) * squreAndMultiply(y, u2 ,p))  % q
        v = pow(g,u1) * pow(y,u2) % p % q
        return v == r % q




# p = 303287
# q = 151643
# # p = 67
# # q = 11
# # p = 283
# # q = 47
# # print(miller_rabin(p))
# # print(miller_rabin(q))
# # print((p - 1) % q)


p, q, g, x, y = genKey()
print(p, q, g, x, y)
r, s = sign('hfadgd', p, q, g, x)
print('r = ' + str(r))
print('s = ' + str(s))

v = verify('hfadgd', r, s, p, q)
print('v = ' + str(v))