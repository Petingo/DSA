## Signing
Assume we have messege $m$
1. pick an hash function $H$
2. Generate a random per-message value $k$ where $1<k<q$
3. $r = (g^k \bmod p)  \bmod q$
4. if $r=0$ , go back to step 2 and pick another $k$
5. $s = (k^{-1} (H(m) + xr))\bmod q$
6. if $s=0$ , go back to step 2 and pick another $k$
7. The signature is $(r, s)$

## Verifying
- reject if $0<r<q$ or $0<s<q$ is not satisfied
- $w = s^{-1} \bmod q$
- $u_1 = H(m) \times w \bmod q$
- $u_2 = r \times w \bmod q$
- $v = ((g^{u_1}\times y^{u_2})\bmod p) \bmod q$
- signature is valid if and only if $v=r$

