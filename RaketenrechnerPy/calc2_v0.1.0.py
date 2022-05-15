import math
import matplotlib.pyplot as plt

rho_W = 997  # kg/m^3
V_T = 0.0015 # m^3   1.5l = 1.5dm³ /1000 = 0.0015m³ Eine Flasche
m_W_s = 1  # kg  Zu einem Drittel gefüllt
V_W_s = m_W_s / rho_W # m^3 = kg/kg/m^3
R = 8.3145   # J/(mol*K) Reynoldzahl
M = 0.028949 # kg/mol Molmasse Luft
T = 293.15   # K entspricht 20°C
p_A = 1*10**5 # Außendruck
p_P = 12*10**5 # Pumpendruck, den man aufpumpt
p_0 = p_A+p_P # Pa Gesamtdruck, also Luftpumpenablesung plus 1
m_L_s = (V_T - V_W_s)*((p_0*M)/(R*T)) # kg
d_D = 2      # mm Düsendurchmesser
A_D = 1/4*math.pi*(d_D/1000)**2  # m^2 = 1/4*pi*(mm/1000=m^2)

d_t = 0.001 # sec
max_t = 15
debug = False

v_str_list = []
t_list = []
V_W_list = []
p_L_list = []
m_L_list = []
# variable Werte:
V_W = V_W_s
m_L = m_L_s
t = 0
while t < max_t:
    rho_L = (m_L)/(V_T-V_W)
    p_L = (rho_L*R*T)/M

    # wässrige Antriebsphase
    if V_W>0:
        v_str = (2*(p_L-p_A)/rho_W)**0.5 # siehe Gl.2@formulas_v2.0.md  
        # m^3 = m/s * m^2 * s
        V_W -= (v_str*A_D*d_t)

    # luftdruckantrieb -> Machzahl beachten = andere Formel!
    else:
        v_str = (2*(p_L-p_A)/rho_L)**0.5
        # kg = m/s*m^2*s*kg/m^3
        m_L -= (v_str*A_D*d_t*rho_L)

    t += d_t

    # debug
    if debug:
        print(f"V_W: {V_W}")
        print(f"m_L: {m_L}")
        print(f"v_str: {v_str}")
        print(f"dV: {(v_str*A_D*d_t)}")
        print(f"rho_L: {rho_L}")
        print(f"p_L: {p_L}")

    # to plot
    v_str_list.append(v_str)
    t_list.append(t)
    V_W_list.append(V_W)
    p_L_list.append(p_L)
    m_L_list.append(m_L)

print(f"Total Iterations: {t/d_t}")
print(rho_L*1000)

fig, axs = plt.subplots(4)
axs[0].plot(t_list, v_str_list, "tab:green")
axs[0].set_title("v_str(m/s)")
axs[1].plot(t_list, V_W_list, "cornflowerblue")
axs[1].set_title("V_W(m^3)")
axs[2].plot(t_list, p_L_list, "tab:red")
axs[2].set_title("p_L(P)")
axs[3].plot(t_list, m_L_list, "royalblue")
axs[3].set_title("m_L(kg)")
plt.show()