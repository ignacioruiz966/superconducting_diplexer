import numpy as np

Amax = 0.04
Amin = 20

w_pass = 2 * np.pi * 8e9
w_cut = 2 * np.pi * 10.5e9

e = np.sqrt( 10**(Amax/10) - 1 )

k = w_pass / w_cut

D = (10**(Amin/10) - 1)/(e**2)

# n = (np.acosh(np.sqrt( D )) / np.acosh(1/k))

n = 7

Y = np.sinh((1 / n) * np.asinh(1 / e))

g = [0] * n

g[0] = 2 * np.sin(np.pi / (2 * n)) / Y

for m in range(2,n + 1):
    num = 4 * np.sin((2 * m - 1) * np.pi / (2 * n)) * np.sin((2 * m - 3) * np.pi / (2 * n))
    dom = g[m - 2] * (Y**2 + np.sin((m - 1) * np.pi / n)**2)
    g[m - 1] = num/dom

Z0 = 50
values = []

for i, gk in enumerate(g):
    k = i + 1
    if k % 2 == 0:
        values.append((gk * Z0 / w_pass) * 1e9)
    else:
        values.append((gk / (Z0 * w_pass)) * 1e12)

Z_0 = 50
h = 0.15e-6
Z_H = 80
Z_L = 5
Lk = 12e-12
c = 3e8
er = 10.3

def microstrip(W_h, er):

    if W_h <= 1:
        er_e = (er + 1) / 2 + (er - 1) / 2 * ((1 + 12 / W_h)**(-0.5) + 0.04 * (1 - W_h)**2)
        Z_m = 60/np.sqrt(er_e) * np.log10(8/W_h + 0.25*W_h)
    else:
        er_e = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 / W_h)**(-0.5)
        Z_m = 120 * np.pi / (np.sqrt(er_e) * (W_h + 1.393 + 0.667 * np.log10(W_h + 1.444)))

    return [Z_m, er_e]

def total_impedance(W, h, er, Lk):
    W_h = W / h
    Zm , ere = microstrip(W_h, er)

    Lm = Zm * np.sqrt(ere) / c
    Lkin = Lk / W
    Cm = np.sqrt(ere) / (c*Zm)
    z_tot = np.sqrt((Lm + Lkin) / Cm)
    vp = 1.0 / np.sqrt((Lm + Lkin) * Cm)
    return [z_tot, vp, Zm, ere]


def find_width(target_Z, h, er, Lk):
    W_arr = np.logspace(-9, -3, 100000)
    best_W =  0
    min_diff = float("inf")
    for W in W_arr:
        Z_tot, vp, Zm, ere = total_impedance(W, h, er, Lk)
        diff = abs(Z_tot - target_Z)
        if diff < min_diff:
            min_diff = diff
            best_W = W
    return best_W

W_H = find_width(Z_H, h, er, Lk) * 1e6
W_L = find_width(Z_L, h, er, Lk) * 1e6

print(W_H)
print(W_L)

lengths = []
for i, gk in enumerate(g):
    k = i + 1
    if k % 2 == 0:
        W = W_H
        Z_tot, vp, Zm, ere = total_impedance(W, h, er, Lk)
        beta_l = gk * Z_0 / Z_H
        length = beta_l * vp / w_pass
    else:
        W = W_L
        Z_tot, vp, Zm, ere = total_impedance(W, h, er, Lk)
        beta_l = gk * Z_L / Z_0
        length = beta_l * vp / w_pass
    lengths.append(length * 1e6)

tot_len = sum(lengths)
for l in lengths:
    print(l)
print(tot_len)