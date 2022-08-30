"""
calc2_v1.1.0.py
(c) 2022 Janik-ux
licensed under MIT license

This program simulates the two dimensional flight of a waterrocket.
"""

from cv2 import MAT_MAGIC_MASK
import matplotlib.pyplot as plt
import rock2_v1_1_0 as rock2
# evtl mit numpy arbeiten


# Beispiel Charts:
# default: d_D=4, m_W_s=0.5, p_P=6*10**5, dt=0.001, verbose=True, debug=False
res = rock2.calc()
fig, axs = plt.subplots(4)
axs[0].plot(res['t_list'], res['a_R_list'], "tab:green")
axs[0].set_title("a_R (m/s^2)")
axs[1].plot(res['t_list'], res['v_R_list'], "cornflowerblue")
axs[1].set_title("v_R (m/s)")
axs[2].plot(res['t_list'], res['h_R_list'], "tab:red")
axs[2].set_title("h_R (m)")
axs[3].plot(res['t_list'], res['a_R_Luft_list'], "royalblue")
axs[3].set_title("a_R_Luft")
plt.show()

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
