import numpy as np 
import sympy as sp 
import matplotlib.pyplot as plt

from scipy import signal

s = sp.symbols('s')
R1, R2, C1, C2 = sp.symbols('R1, R2, C1, C2', positive=True)
V_in, V1, V2 = sp.symbols('V_in V1 V2')

Zc1 = 1/(s*C1)
Zc2 = 1/(s*C2)

# Enforce Vout = V2 (unity follower)
# Enforce Vout = V2 (unity follower)
eq1 = (V1 - V_in)/Zc1 + (V1 - V2)/Zc2 + (V1 - V2)/R1
eq2 = (V2 - V1)/Zc2 + V2/R2

sol = sp.solve([sp.Eq(eq1,0), sp.Eq(eq2,0)], (V1, V2), dict=True)[0]
H_sym = sp.simplify(sol[V2]/V_in)

# Symbolic polynomials(
num_sym, den_sym = sp.fraction(sp.simplify(H_sym))
num_poly = sp.Poly(sp.expand(num_sym), s)
den_poly = sp.Poly(sp.expand(den_sym), s)

# numerik values 
C1_Val = 470e-9
C2_val = 470e-9
R1_val = 4.7e6
R2_val = 10e6
subs = {C1: C1_Val, C2: C2_val, R1:R1_val, R2:R2_val}

num_coeffs = [float(c) for c in sp.Poly(sp.N(num_poly.as_expr().subs(subs)), s).all_coeffs()]
den_coeffs = [float(c) for c in sp.Poly(sp.N(den_poly.as_expr().subs(subs)), s).all_coeffs()]

a2, a1, a0 = den_coeffs
w0 = np.sqrt(a0/a1)
fc = w0 / (2*np.pi)
Q = w0 / (a1/a2)

print("fc (Hz) =", fc)
print("Q =", Q)

system = signal.TransferFunction(num_coeffs, den_coeffs)
f = np.logspace(-3, 3, 2000)
w = 2*np.pi*f
w_out, mag, phase = signal.bode(system, w)

plt.figure(figsize=(10,5))
plt.semilogx(w_out/(2*np.pi), mag)
plt.title('Bode Magnitude - Unity Gain Sallen-Key HPF (computed)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(which='both', linestyle=':')
plt.axvline(fc, linestyle='--', linewidth=1)
plt.show()

plt.figure(figsize=(10,5))
plt.semilogx(w_out/(2*np.pi), phase)
plt.title('Bode Phase - Unity Gain Sallen-Key HPF (computed)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (deg)')
plt.grid(which='both', linestyle=':')
plt.show()