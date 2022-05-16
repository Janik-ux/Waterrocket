"""
calc2_v1.0.0.py 
(c) 2022 Janik-ux
licensed under MIT license

This program simulates the one dimensional flight of a waterrocket.
"""

import math
import matplotlib.pyplot as plt

rho_W = 997  # kg/m^3
V_T   = 0.0015 # m^3   1.5l = 1.5dm³ /1000 = 0.0015m³ Eine Flasche
m_W_s = 0.5  # kg  Zu einem Drittel gefüllt
V_W_s = m_W_s / rho_W # m^3 = kg/kg/m^3
R     = 8.3145   # J/(mol*K) Reynoldzahl
M     = 0.028949 # kg/mol Molmasse Luft
T     = 293.15   # K entspricht 20°C
p_A   = 1*10**5 # Außendruck
p_P   = 12*10**5 # Pumpendruck, den man aufpumpt
p_0   = p_A+p_P # Pa Gesamtdruck, also Luftpumpenablesung plus 1
m_L_s = (V_T - V_W_s)*((p_0*M)/(R*T)) # kg
d_D   = 5      # mm Düsendurchmesser
A_D   = 1/4*math.pi*(d_D/1000)**2  # m^2 = 1/4*pi*(mm/1000=m^2)
g     = 9.81

m_Struktur = 0.15 # kg Masse der leeren Flasche
m_Nutz     = 0 # Masse der Nutzlast
m_R_s      = m_Struktur+m_Nutz+m_L_s+m_W_s # Flasche + Nutzlast + Wasser + Luft
dt         = 0.0001 # sec
max_t      = 20 # wie lange soll simuliert werden
debug      = False

v_str_list = []
t_list     = []
V_W_list   = []
p_L_list   = []
m_L_list   = []
h_R_list   = []
v_R_list   = []
a_R_list   = []
m_R_list   = []

# variable Werte:
h_R = 0 # m Höhe der Rakete 0 Meter
v_R = 0 # m/s Geschwindigkeit der Rakete
m_R = m_R_s # Masse Rakete
V_W = V_W_s # Volumen Wasser
m_L = m_L_s # Masse Luft
t   = 0
while t < max_t and h_R>=0: # and float(h_R) > -0.5
    rho_L = (m_L)/(V_T-V_W)
    p_L = round((rho_L*R*T)/M, 10) # round because of the bad rounding of a computer

    if p_L < p_A:
        print(f"p_L < p_A ({p_L})")
        p_L = p_A # sure not right, but otherwise it would produce complex numbers in v_str
        rho_L = (p_L*M)/(R*T) # all values match them outside the rocket
        m_L = rho_L*V_T # V_W has to be 0, so V_T-V_W = V_T


    # wässrige Antriebsphase
    if V_W>0:
        v_str = (2*(p_L-p_A)/rho_W)**0.5 # siehe Gl.2@formulas_v2.0.md
        # m^3 = m/s * m^2 * s
        dV_W = (v_str*A_D*dt) # Volumenabfluss des Wassers
        # m/s = m^3*kg/m^3*m/s/kg
        dv_R = ((dV_W*rho_W*v_str)/m_R) - g*dt # Geschwindigkeitszuwachs
        
        V_W -= dV_W
        if V_W < 0:
            dV_W += V_W # dV_W muss auf null kommen, sonst wird zu viel masse abgezogen
            print(f"V_W < 0! ({V_W})")
            V_W = 0 # kann nicht kleiner als null werden
        m_R -= dV_W*rho_W

    # luftdruckantrieb -> Machzahl beachten = andere Formel!
    else:
        v_str = (2*(p_L-p_A)/rho_L)**0.5
        if 2*(p_L-p_A)/rho_L < 0:
            print(f"p_L: {p_L}, p_A: {p_A}, rho_L: {rho_L}")
        # kg = m/s*m^2*s*kg/m^3
        dm_L = (v_str*A_D*dt*rho_L)
        # m/s = m^3*kg/m^3*m/s/kg
        dv_R = ((dm_L*v_str)/m_R) - g*dt # Geschwindigkeitszuwachs

        m_L -= dm_L
        m_R -= dm_L
    
    v_R += dv_R
    h_R += v_R*dt

    t += dt

    # debug
    if debug:
        print(f"V_W: {V_W}")
        print(f"m_L: {m_L}")
        print(f"v_str: {v_str}")
        print(f"dV: {(v_str*A_D*dt)}")
        print(f"rho_L: {rho_L}")
        print(f"p_L: {p_L}")

    # to plot
    v_str_list.append(v_str)
    t_list.append(t)
    V_W_list.append(V_W)
    p_L_list.append(p_L)
    m_L_list.append(m_L)
    v_R_list.append(v_R)
    a_R_list.append(dv_R/dt) # m/s/dt(s)/dt(s)=m/s/s=m/s^2
    h_R_list.append(h_R)
    m_R_list.append(m_R)


print(f"Total Iterations: {round(t/dt, 0)}")
# print(p_L_list)

# äußere Werte
fig, axs = plt.subplots(4)
axs[0].plot(t_list, a_R_list, "tab:green")
axs[0].set_title("a_R (m/s^2)")
axs[1].plot(t_list, v_R_list, "cornflowerblue")
axs[1].set_title("v_R (m/s)")
axs[2].plot(t_list, h_R_list, "tab:red")
axs[2].set_title("h_R (m)")
axs[3].plot(t_list, m_R_list, "royalblue")
axs[3].set_title("m_R (kg)")
plt.show()

# innere Werte
# fig, axs = plt.subplots(4)
# axs[0].plot(t_list, v_str_list, "tab:green")
# axs[0].set_title("v_str(m/s)")
# axs[1].plot(t_list, V_W_list, "cornflowerblue")
# axs[1].set_title("V_W(m^3)")
# axs[2].plot(t_list, p_L_list, "tab:red")
# axs[2].set_title("p_L(P)")
# axs[3].plot(t_list, m_L_list, "royalblue")
# axs[3].set_title("m_L(kg)")
# plt.show()
