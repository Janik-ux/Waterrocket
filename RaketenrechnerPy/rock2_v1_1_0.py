"""
calc2_v1.1.0.py
(c) 2022 Janik-ux
licensed under MIT license

This program simulates the two dimensional flight of a waterrocket.
"""

import math
# evtl panda benutzen


def calc(dt=0.001, m_W_s=0.5, p_P=6*10**5, d_D=4, c_w_R=0.2, V_T=0.0015, debug=False, verbose=True) -> dict:
    # "naturkonstanten" und Umwelteinflüsse
    R     = 8.3145   # J/(mol*K) Reynoldzahl
    M     = 0.028949 # kg/mol Molmasse Luft
    rho_W = 997  # kg/m^3
    rho_L_A = 1.2 # kg/m^3 Dichte der Umgebungsluft
    p_A   = 1*10**5 # Pa Außendruck
    g     = -9.81   # Erdbeschleunigung
    T     = 293.15   # K entspricht 20°C

    # Raketenspezifikationen
    # V_T   = 0.0015 # m^3 Tankvolumen (1.5l = 1.5dm³ /1000 = 0.0015m³)
    # m_W_s = 0.5  # kg Masse Füllwasser
    m_Struktur = 0.15 # kg Masse der leeren Flasche
    m_Nutz     = 0 # Masse der Nutzlast
    # p_P   = 6*10**5 # Pumpendruck, den man aufpumpt
    A_R   = 0.00785 # m^2 1/4*pi*(10cm/100)^2 = m^2 Fläche der Rakete in Strömungsrichtung
    # d_D   = 4      # mm Düsendurchmesser
    # c_w_R = 0.2 # Luftwiderstandsbeiwert der Rakete

    # Einstellungen
    # dt         = 0.001 # 0.001 reicht imho aus. the smaller, the longer the program is running
    max_t      = 20 # wie lange soll simuliert werden
    # debug      = False
    calculate_LW = True # Luftwiderstand berechnen

    # vom Programm berechnete Werte
    p_0   = p_A+p_P # Pa Gesamtdruck, also Luftpumpenablesung plus 1
    V_W_s = m_W_s / rho_W # m^3 = kg/kg/m^3
    m_L_s = (V_T - V_W_s)*((p_0*M)/(R*T)) # kg
    A_D   = 1/4*math.pi*(d_D/1000)**2  # m^2 = 1/4*pi*(mm/1000=m^2)
    m_R_s = m_Struktur+m_Nutz+m_L_s+m_W_s # Flasche + Nutzlast + Wasser + Luft

    # initialisieren der Speicherstrukturen für die Werte
    v_str_list    = []
    t_list        = []
    V_W_list      = []
    p_L_list      = []
    m_L_list      = []
    h_R_list      = []
    v_R_list      = []
    a_R_list      = []
    m_R_list      = []
    a_R_Luft_list = []
    twr_list      = []


    # Über die Berechnung variable Werte:
    h_R = 0 # m Höhe der Rakete 0 Meter
    v_R = 0 # m/s Geschwindigkeit der Rakete
    m_R = m_R_s # Masse Rakete
    V_W = V_W_s # Volumen Wasser
    m_L = m_L_s # Masse Luft
    t   = 0

    # Schleife für numerische Integration über dt (Ich hab keine Ahnung was das ist, aber klingt gut)
    while t < max_t and h_R>=0:
        rho_L = (m_L)/(V_T-V_W) # Dichte des Wassers bei gegebenem Volumen
        p_L = round((rho_L*R*T)/M, 10) # round because of the division problem of a computer (1.00000000001)

        # Druckausgleich?
        if p_L < p_A:
            if (verbose):
                print(f"Druckausgleich nach {t} Sekunden:", f"p_L < p_A ({p_L})")

            p_L = p_A # sure not right, but otherwise it would produce complex numbers in v_str
            rho_L = (p_L*M)/(R*T) # all values match them outside the rocket
            m_L = rho_L*V_T # V_W has to be 0, so V_T-V_W = V_T

        # Bremsung durch Luft
        if calculate_LW:
            # Berechnung des Geschwindigkeitsverlustes durch die Umgebungsluft
            richtung = -1 if v_R > 0 else 1 # durch Quadrat verliert v_R Vorzeichen in der nächsten Rechung
            F_Luft = (1/2*rho_L_A*A_R*c_w_R*v_R**2)*richtung
            # print(F_Luft)
            # v = F/m*t
            dv_R_Luft = F_Luft/m_R*dt
        else:
            dv_R_Luft = 0


        # wässriger Antrieb
        if V_W>0:
            # Austrittsgeschwindigkeit
            v_str = (2*(p_L-p_A)/rho_W)**0.5 # siehe Gl.2@formulas_v2.0.md

            # Volumenabfluss des Wassers
            # m^3 = m/s * m^2 * s
            dV_W = (v_str*A_D*dt)

            # Kraft durch Rückstoß von Strahl erzeugt
            F_R_str = dV_W*rho_W*v_str

            # Geschwindigkeitszuwachs durch v_str
            # m/s = m^3*kg/m^3*m/s/kg
            dv_R_str = F_R_str/m_R

            dm_L = 0 # Die Luft kann noch nicht ausströmen


        # luftdruckantrieb -> Machzahl beachten = andere Formel!
        else:
            # Austrittsgeschwindigkeit
            v_str = (2*(p_L-p_A)/rho_L)**0.5

            # Massenabfluss der Luft
            # kg = m/s*m^2*s*kg/m^3
            dm_L = (v_str*A_D*dt*rho_L)

            # Kraft durch Rückstoß von Strahl erzeugt
            F_R_str = (dm_L*v_str)

            # Geschwindigkeitszuwachs durch v_str
            # m/s = m^3*kg/m^3*m/s/kg
            dv_R_str = (F_R_str/m_R) # Geschwindigkeitszuwachs durch v_str

            dV_W = 0 # Wasser ist schon alle

        twr = abs(F_R_str)/abs(g*dt*m_R)

        # Veränderung der Geschwindigkeit der Rakete
        dv_R = dv_R_str + g*dt + dv_R_Luft

        # Ändern der Geschwindigkeits und Höhenwerte
        v_R += dv_R
        h_R += v_R*dt

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
        a_R_Luft_list.append(dv_R_Luft/dt)
        twr_list.append(twr)

        # Variablen wieder anpassen
        V_W -= dV_W
        if V_W < 0:
            dV_W += V_W # dV_W muss auf null kommen, sonst wird zu viel masse abgezogen
            if verbose:
                print(f"V_W < 0! ({V_W})")
                print(f"Wasser leer nach {t} Sekunden")
            V_W = 0 # kann nicht kleiner als null werden
        m_R -= dV_W*rho_W
        m_R -= dm_L
        m_L -= dm_L

        # Zeit schreitet voran
        t += dt


    if debug:
      print(f"Total Iterations: {round(t/dt, 0)}")
      # print(p_L_list)

    max_height = max(h_R_list)
    if verbose:
        print('Max Höhe:', max_height)
    return {
        'max_height': max_height,
        't_list': t_list,
        'a_R_list': a_R_list,
        'v_R_list': v_R_list,
        'h_R_list': h_R_list,
        'a_R_Luft_list': a_R_Luft_list,
        'twr_list': twr_list
        }
