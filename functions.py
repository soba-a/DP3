import math as m
import sympy as sp

def calc_kv(d, w): # THIS IS DIMENSIONLESS !!!!!
    return (3.56 + (calc_V(d, w))**0.5) / 3.56

def calc_V(d, w): # THIS IS IN M/S!!!!!
    return d/2 * w / 1000

def calc_Wt(d, T): # MAKE SURE YOU'RE IN N AND MM!!!!!
    return T / (d/2)

def calc_sig_bend(Wt, ko, kv, ks, b, mod, kh, kb, yj):
    return (Wt * ko * kv * ks) * (1 / (b * mod)) * ((kh * kb) / yj)

def calc_sig_contact(ze, wt, ko, kv, ks, kh, d1, b, zr, zi):
    return ze * ((wt * ko * kv * ks) * (kh / (d1 * b)) * (zr / zi))**0.5

def calc_Sf(Yn, Kt, sigma): #hardcoded for given values
    return 210 * (Yn/Kt) * (1/sigma)

def calc_Sf2(Yn, Kt, b, m, Yj, Wt, Ko, Kv, Ks, Kh, Kb): # hardcoded for given values
    return 210 * (Yn/Kt) * (((b*m*Yj)/(Wt*Ko*Kv*Ks*Kh*Kb)))

def calc_Sfb(Yn, Kt, Sf, m, Yj, Wt, Ko, Kv, Ks, Kh, Kb): # hardcoded for given values
    return (210 * (Yn/Kt) * (((m*Yj)/(Wt*Ko*Kv*Ks*Kh*Kb * Sf))))**(-1)

def calc_Sh(Zn, Ch, Kt, sigma): #hardcoded for given values
    return 760 * (Zn * Ch) / Kt * (1 / sigma)

def calc_Sh2(Zn, Ch, Kt, Ze, Wt, Ko, Kv, Ks, Kh, Zr, dw1, b, Zi): #hardcoded for given values
    return 760 * ((Zn * Ch) / Kt) * (1/Ze) * (((Wt * Ko * Kv * Ks * Kh * Zr) / (dw1 * b * Zi))**-0.5)

def calc_Shb(Zn, Ch, Kt, Ze, Wt, Ko, Kv, Ks, Kh, Zr, dw1, Sh, Zi): #hardcoded for given values
    b = sp.symbols('b')
    eq = (760 * ((Zn * Ch) / Kt) * (1/Ze) * (((Wt * Ko * Kv * Ks * Kh * Zr) / (dw1 * b * Zi))**-0.5)) - Sh
    sol = sp.solve(eq, b)
    return sol[0]

def calc_Zi(phi, mg, mn):
    return ((m.cos(m.radians(phi)) * m.sin(m.radians(phi))) / (2 * mn)) * ((mg)/(mg+1))