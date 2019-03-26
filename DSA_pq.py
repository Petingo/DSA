import hashlib
import random, sys

# set recursion limit to 10000 or it will reach the init limit 1000 when running extend_gcd()
sys.setrecursionlimit(10000)

# square and multiply（快速冪）
# x ^ h mod n
def fast_pow(x, h, n):
    y = 1
    h = bin(h)[2:] # convert h into binary
    for i in range(len(h)):
        y = (y ** 2) % n
        if h[i] == '1':
            y = (y * x) % n

    return y

# 歐幾里得算法（輾轉相除法）
def gcd(a, b):
	while b != 0:
		a, b = b, a % b
	return a

# 擴展歐幾里得算法
def extend_gcd(a, b):
     if b == 0:
         return 1, 0, a
     else:
         x, y, gcd = extend_gcd(b, a % b)
         x, y = y, (x - (a // b) * y)
         return x, y, gcd

# 求 a 對同於 m 的乘法反元素
def invert(a, m):
    x, y, gcd = extend_gcd(a, m)
    if (gcd == 1):
        return x % m
    else:
        return None

# miller-rabin test，用於驗證質數
def miller_rabin_test(n, confidence=40):
    k = 0
    m = (n - 1)
    while m % 2 == 0:
        m = m // 2
        k = k + 1
    while confidence > 0:
        # choose only odd a
        a = random.randrange(n - 4) + 2
        while a % 2 == 0:
            a = random.randrange(n - 4) + 2

        b = fast_pow(a, m, n)

        if b != 1 and b != n - 1:
            i = 1
            while i < k and b != n - 1:
                b = (b ** 2) % n
                if b == 1:
                    return False
                i = i + 1

            if b != n - 1:
                return False

        confidence -= 1

    return True

# 生成大質數
def gen_big_prime(bits=1024):
    tmp = random.getrandbits(bits)
    # if the prime < 5, there will be an error when running 'random.randrange(n - 4) + 2' in miller_rabin_test() 
    while len(bin(tmp))-2 != bits or tmp < 5 or miller_rabin_test(tmp) == False:
        tmp = random.getrandbits(bits)
    return tmp

def sha_string_to_int(m):
    return int(hashlib.sha1(m.encode()).hexdigest(), 16)

def sha(n):
    return hashlib.sha1(bin(n).encode())

def sha_to_int(n):
    return int(sha(n).hexdigest(), 16)

def gen_param(L=1024):
    found = False
    while not found:
        S = random.getrandbits(20)
        q = gen_big_prime(160)

        n = (L-1) // 160
        b = (q >> 5) & 15
        C = 0
        N = 2
        V = {}
        powb = pow(2, b)
        powL1 = pow(2, L-1)

        while C < 4096:
            for k in range(0, n+1):
                V[k] = sha_to_int(S + N + k)
            W = V[n] % powb
            for k in range(n-1, -1, -1):
                W = (W << 160) + V[k]
            X = W + powL1
            p = X-(X % (2 * q) - 1)
            if(powL1 <= p and miller_rabin_test(p)):
                found = True
                break;
            C += 1
            N += n + 1
    return p, q

def gen_key():
    p, q = gen_param()
    g = fast_pow(2, (p - 1) // q, p)
    x = random.randrange(1, q)
    y = fast_pow(g, x, p)
    return p, q, g, x, y

def sign(m, p, q, g, x):
    s = 0
    while s == 0:
        k = random.randrange(2, q)
        r = fast_pow(g, k, p) % q
        s = invert(k, q) * (sha_string_to_int(m) + x * r) % q
    return r, s

def verify(m, r, s, p, q):
    if not (0 < r < q or 0 < s < q):
        print("fail (0 < r < q or 0 < s < q) not satisfied")

    w = invert(s, q)
    u1 = (sha_string_to_int(m) * w) % q
    u2 = (r * w) % q
    v = ((fast_pow(g, u1, p) * fast_pow(y, u2, p)) % p) % q
    
    # print("v =", v)
    return v == r

if __name__ == "__main__":    
    print("keys:")
    p, q, g, x, y = gen_key()
    print("p =", p)
    print("q =", q)
    print("g =", g)
    print("x =", x)
    print("y =", y)
    # print("d =", p % q)

    print("\nsign:")
    m = "myDSAbooo"
    r, s = sign(m, p, q, g, x)
    print("m =", m)
    print("r =", r)
    print("s =", s)

    print("\nverify:")
    v = verify(m, r, s, p, q)
    print("v =", v)