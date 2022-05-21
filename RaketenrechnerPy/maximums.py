import matplotlib.pyplot as plt
import rock2_v1_1_0 as rock2
# evtl mit numpy arbeiten

###############################################################################

# welches dt ist sinnvoll?
# for i in range(6):
#     dt = 1/(10**i)
#     res = rock2.calc(dt=dt)
#     print(dt, res['max_height'])


###############################################################################

# Wie viel Wasser ist sinnvoll (Druck immer gleich)
#
V_T = 0.01  # 10 Liter Flasche 💪
step_m = 0.1 # kg Stepsize Wasser
range_m = int((V_T * 1000) / step_m)
x = []
y = []
for i in range(range_m):
    m_W_s = step_m * i
    res = rock2.calc(m_W_s=m_W_s, p_P=300*10**5, V_T=V_T, verbose=False)
    print(m_W_s, res['max_height'])
    x.append(m_W_s)
    y.append(res['max_height'])

plt.plot(x, y)
plt.title("Wasser(l) vs. Höhe")
plt.xlabel("Wasser (l)")
plt.ylabel("Höhe (m)")
plt.show()

###############################################################################

# Wie viel Druck ist sinnvoll (Wasser immer gleich)
# Bei 0.5 Wasser braucht es zB 2,5 bar Druck, um abzuheben.
# exponentiell unendlicher Druck bringt unendliche Höhe
# x = []
# y = []
# for i in range(10):
#     p_P = i * 10**5
#     res = rock2.calc(p_P=p_P, m_W_s=0.5)
#     print(p_P, res['max_height'])
#     x.append(p_P/100000)
#     y.append(res['max_height'])

# plt.plot(x, y)
# plt.title("Anfangsdruck (bar) vs. Höhe")
# plt.show()

###############################################################################

# Welche Düse ist sinnvoll (Wasser und Druck immer gleich)
# interessanter Weise ist offenbar der größte Durchmesser der beste
# bis zu einem cw von 0,5 (drüber hinaus wirdv viel weniger,sodass sich eine Düse lohnt)
# -> das heißt,man braucht keine Rakete, sondern kann das Ding von einem festem Medium abschießen
#
# Rakete:
#  A
# | |
# | |
# | |
#
# festes Medium:
#    #
#    #
#  #####
#
# zusammen:
#
#   A
#  | |
#  |#|
#  |#|
# #####
#
#
# für größere Werte als 30mm ist aber wahrscheinlich die Formel nicht mehr sinnvoll
#
# x = []
# y = []
# for i in range(30):
#     d = i
#     res = rock2.calc(d_D=d, c_w_R=0.3)
#     # print(d, res['max_height'])
#     x.append(d)
#     y.append(res['max_height'])
#     # y.append(res["max_twr"])

# print(y)
# plt.plot(x, y)
# plt.title("Düse (mm) vs. Höhe")
# plt.show()

###############################################################################

# wasser und Druck vs Höhe
# egal wie der Druck ist, 0.5 Wasser scheint immer ganz gut sein
# bei niedrigeren Drücken, etwas weniger Wasser.
# max_w = 15 # Deziliter aka 0.1kg um int bei Druck zu haben has to be int!
# max_p = 20 # bar
# data = [[0] * max_w for i in range(max_p)]
# print(data)
# for i in range(max_p):
#     for j in range(max_w):
#         p_P = i * 10**5
#         m_W_s = j * 0.1

#         res = rock2.calc(p_P=p_P, m_W_s=m_W_s, verbose=False)
#         data[i][j] = res['max_height']

# plt.imshow(data)
# plt.title("Druck und Wasser vs. Höhe")
# plt.xlabel("Wasser (Deziliter)")
# plt.ylabel("Druck (bar)")
# cbar = plt.colorbar()
# cbar.set_label('Höhe (m)')

# plt.show()


###############################################################################

# Düse und cw-Wert vs Höhe

# max_d = 30  # mm Düsendurchmesser
# max_cw = 1  # cw-Wert
# d_cw = 0.05  # cw-Wert Stepsize
# range_cw = int(max_cw / d_cw)
# data = [[0] * max_d for i in range(range_cw)]
# for i in range(range_cw):
#     for j in range(max_d):
#         cw = i * d_cw
#         d = j

#         res = rock2.calc(d_D=d, c_w_R=cw, verbose=False, p_P=6*10**5, m_W_s=0.5,)
#         print(i,j, d, cw, res['max_height'])
#         data[i][j] = res['max_height']

# print(data)
# plt.imshow(data, extent=[0, max_d, max_cw, 0], aspect=max_d/max_cw)
# plt.title("Düse und cw vs. Höhe")
# plt.xlabel("Durchmesser Düse (mm)")
# plt.ylabel("cw Rakete")
# cbar = plt.colorbar()
# cbar.set_label('Höhe (m)')
# plt.show()

###############################################################################

# Flaschengröße und Wasseranteil vs Höhe (unterschiedliches Leergewicht vernachlässigt)
#
# Bei größeren Flaschen scheint 10% Wasser optimal zu sein. (Falls die auch so viel wiegen wie die kleine Flasche)
#
# Flaschen größer 50 Liter sind bei 6 bar nicht mehr sinnvoll
# max_w   = 1  # Max-Anteil Volumen Wasser
# d_w     = 0.01  # Stepsize Anteil Volumen Wasser
# range_w = int(max_w / d_w)

# min_V   = 0.0005
# max_V   = 0.100  # Gesamt Volumen der Flasche ( 100 Liter!!)
# d_V     = 0.001  # Volumen Stepsize
# range_V = int((max_V - min_V) / d_V)

# data = [[0] * range_w for i in range(range_V)]
# for i in range(range_V):
#     for j in range(range_w):
#         v = i * d_V + min_V
#         w = j * d_w * v * 1000

#         res = rock2.calc(m_W_s=w, V_T=v, verbose=False)
#         print(i,j, v, w, res['max_height'])
#         data[i][j] = res['max_height']

# plt.imshow(data)
# plt.xlabel("Anteil Volumen Wasser (m^3)")
# plt.ylabel("Gesamt Volumen der Flasche (m^3)")
# plt.title("Wasseranteil und GesamtVolumen vs. Höhe")
# plt.show()

###############################################################################

# Beispiel Charts:
# res = rock2.calc(V_T=0.010, m_W_s=2)
# fig, axs = plt.subplots(4)
# axs[0].plot(res['t_list'], res['a_R_list'], "tab:green")
# axs[0].set_title("a_R (m/s^2)")
# axs[1].plot(res['t_list'], res['v_R_list'], "cornflowerblue")
# axs[1].set_title("v_R (m/s)")
# axs[2].plot(res['t_list'], res['h_R_list'], "tab:red")
# axs[2].set_title("h_R (m)")
# axs[3].plot(res['t_list'], res['a_R_Luft_list'], "royalblue")
# axs[3].set_title("a_R_Luft")
# plt.show()

# innere Werte
# fig, axs = plt.subplots(4)
# axs[0].plot(res['t_list'], v_str_list, "tab:green")
# axs[0].set_title("v_str(m/s)")
# axs[1].plot(res['t_list'], V_W_list, "cornflowerblue")
# axs[1].set_title("V_W(m^3)")
# axs[2].plot(res['t_list'], p_L_list, "tab:red")
# axs[2].set_title("p_L(P)")
# axs[3].plot(res['t_list'], m_L_list, "royalblue")
# axs[3].set_title("m_L(kg)")
# plt.show()
