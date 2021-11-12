import scipy.constants as constants
import math
import matplotlib.pyplot as plt
# ----inital data----
# not to be changed from code itself
# here configure youir rocket data
startmasse  = 1.745 # kg
leermasse   = 0.445 # kg
dichte      = 1000 # kg/m^3
initialpressure = 15 * 10**5 # Pa
breakSecond = 5
duesendurchmesser = 0.022 # m
duesenflaeche     = math.pi * (duesendurchmesser/2)**2 # m^2 unter Annahme einer runden Düse
step = 0.1 # wie genau auflösen? 1 sekunde # TODO ist wahrscheinlich zu ungenau

# matplotlib
x_list = []
twr_list = []
Vrakete_list = []

# daten für iterative vorgehensweise
# vars to be changed every iteration
masse       = startmasse # gramm
second      = step
pressure    = initialpressure
Vrakete     = 0 # m/s

# powered ascend
while second <= breakSecond:
    print("----------Sekunde: {}----------".format(second))
    # iterieren pro sekunde

    # berechnen:
    Vwasser = (2*pressure/dichte)**0.5 # m/s keine Ahnung, warum man den Durchmesser nicht braucht 
                                  # siehe auch https://www.physikerboard.de/topic,45753,-wasserstrahlaustrittsgeschwindigkeit-einer-1mm-duese.html
    austrMasse = duesenflaeche * Vwasser * step * dichte # kg weil m^2 * m/s * 1s = m^3, m^3*kg/m^3=kg
    thrust = austrMasse*Vwasser # kg*m/s = N
    twr = thrust/(masse*constants.g)
    beschleunigung = -thrust/masse*step
    Vrakete += beschleunigung # impulsänderung durch Wasseraustritt (+m/s)
    Vrakete -= constants.g*step # impulsänderung durch Gravitation (-m/s)

    # auswerten:
    print("Vrakete: {} m/s,\nVwasser: {} m/s,\nbeschleunigung: {} m/s^2,\nTWR: {},\naustrMasse: {} kg,\nmasse: {} kg\n".format(round(Vrakete, 2), round(Vwasser, 2), round(beschleunigung, 2), round(twr, 2), round(austrMasse, 2), round(masse, 2)))
    x_list.append(second)
    twr_list.append(twr)
    Vrakete_list.append(Vrakete)

    # vars für nächsten step bereit machen
    masse -= austrMasse
    # if masse <= leermasse:
    #     break # quickfix normal mit druck regeln, sodass einfach keine austrMasse mehrabgezogen wird.
    second += step
    second = round(second, 1)

plt.plot(x_list, twr_list)
plt.plot(x_list, Vrakete_list)
plt.legend(["TWR", "Vrakete"])
plt.title("Waterrocket data")
plt.show()