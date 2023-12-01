import sympy as sp
import numpy as np
import math as m
from functions import *

# use 10mm shaft
d_shaft = 10

g1_motor = {'mod': 1, 'n': 76, 'pd': 76, 'od': 78, 'F': 10, 'p_a': 20, 'Y': 0.435}
g2_shaft = {'mod': 1, 'n': 55, 'pd': 55, 'od': 57, 'F': 10, 'p_a': 20, 'Y': 0.415}
#https://www.mcmaster.com/2664N373/ 76
#https://www.mcmaster.com/2664N369/ 55

w_blade = 4600 # RPM
w_motor = w_blade / (g1_motor['n'] / g2_shaft['n'])

print("Initial Requirements Check: RPM & minimum diameter")
print(w_motor , 'compared to 3000 - 3500 RPM' ) # RPM
# diameter check on paper

#lewis
# d2 = g2_shaft['pd']
# K_v = calc_kv(d2, w_blade * 2 * m.pi / 60)
# print("K_v: ", K_v)
# W_t = calc_Wt(d2, 1548)
# F = g2_shaft['F']
# Y = g2_shaft['Y']
# sig_lewis = (K_v * W_t)  / (F * 1 * Y)

# loads
W_t = calc_Wt(g2_shaft['pd'], 1548)
print("W_t:", W_t)
W_r = W_t * m.tan(m.radians(g2_shaft['p_a']))
print("W_r:", W_r)

# AGMA pinion
ko = 1
kv = calc_kv(g2_shaft['pd'], 4600 * 2 * m.pi / 60) # double check
print("kv", kv)
ks = 1
b = 10
kh = 1.2304 #1.2775
kb = 1
yj = 0.442
mod = 1
d1 = g2_shaft['pd']
zr = 1
zi = calc_Zi(20, 76/55, 1)
print("zi", zi)
ze = 191
Yn = 0.9095 # based on bearing cycles
Kt = 1
Zn = 0.8649 # based on bearing cycles
Ch = 1


sigmab = calc_sig_bend(W_t, ko, kv, ks, b, mod, kh, kb, yj)
sigmac = calc_sig_contact(ze, W_t, ko, kv, ks, kh, d1, b, zr, zi)

Sf = calc_Sf(Yn, Kt, sigmab)
Sh = calc_Sh(Zn, Ch, Kt, sigmac)
Sf2 = calc_Sf2(0.9095, 1, 10, 1, 0.442, 56.291, 1, 2.022, 1, 1.2304, 1)
Sh2 = calc_Sh2(0.8649, 1, 1, 191, 56.291, 1, 2.022, 1, 1.2304, 1, 55, 10, 0.0932)
print("Pinion Sf: ", Sf, Sf2)
print("Pinion Sh: ", Sh, Sh2)

Sfb = calc_Sfb(0.9095, 1, 2, 1, 0.442, 56.291, 1, 2.022, 1, 1.2304, 1)
Shb = calc_Shb(0.8649, 1, 1, 191, 56.291, 1, 2.022, 1, 1.2304, 1, 55, 2, 0.0932)
print("Pinion Sfb: ", Sfb)
print("Pinion Shb: ", Shb)


#LOADS
g2_facewidth = g2_shaft['F']
bearing_width = 9

W = sp.Matrix([W_t, 0, -1*W_r])
Fb = sp.Matrix([15.62, 0, 39.85])
Tb = sp.Matrix([0, -1548, 0])
Fa = sp.Matrix([0, 10, 0])
Ma = sp.Matrix([1016, 0, 0])

r1x,r1y,r1z,r2x,r2y,r2z = sp.symbols('r1x r1y r1z r2x r2y r2z')
R1 = sp.Matrix([r1x, r1y, r1z]).subs(r1y, 0)
R2 = sp.Matrix([r2x, r2y, r2z]).subs(r2y, 0)

W_loc = sp.Matrix([0, -(g2_facewidth/2 + 3 + bearing_width/2), 0]) # to do
Fb_loc = sp.Matrix([0, 100 - bearing_width + 15 + bearing_width/2, 0]) # to do
R2_loc = sp.Matrix([0, 100 - bearing_width, 0]) # to do

# Sum of forces is 0
sumF = W + R1 + R2 + Fb
print("sumF: ", sumF)

# Sum of moments is 0
sumM = W_loc.cross(W) + Fb_loc.cross(Fb) + R2_loc.cross(R2) + Ma + Tb
print("W_loc:", W_loc.cross(W))
print("Fb_loc:", Fb_loc.cross(Fb))
print("R2_loc:", R2_loc.cross(R2))
print("sumM: ", sumM)

# Solve for R1 and R2
sol = sp.solve([sumF[0], sumF[2], sumM[0], sumM[2]], [r1x, r1z, r2x, r2z])
print("Solution to system:", sol)

b1_rad = (sol[r1x]**2 + sol[r1z]**2)**0.5
b2_rad = (sol[r2x]**2 + sol[r2z]**2)**0.5
print("R1 Radial Load:",b1_rad)
print("R2 Radial Load:",b2_rad)

b_revs = 4600 * 20000 * 60

C10_b1 = b1_rad * (b_revs / (1*10**6))**(1/3)
C10_b2 = b2_rad * (b_revs / (1*10**6))**(1/3)
print("Bearing 1 Basic Dynamic:", C10_b1)
print("Bearing 2 Basic Dynamic:", C10_b2)
