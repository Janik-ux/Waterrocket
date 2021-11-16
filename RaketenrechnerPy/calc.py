import scipy.constants as constants
import math
import matplotlib.pyplot as plt
# ----inital data----
# not to be changed from code itself
# here configure youir rocket data
dichte      = 1000 # kg/m^3
wasserfuellanteil = 1/3
luftfuellanteil = 1-wasserfuellanteil
leermasse   = 0.445 # kg
gesamtvolumen = 4.6 * 10**-3 # L * 10^-3 = m^3
wassermasse = gesamtvolumen*wasserfuellanteil*dichte
startmasse = wassermasse + leermasse
initialLuftvolumen = gesamtvolumen*luftfuellanteil
initialpressure = 15 * 10**5 # Pa
duesendurchmesser = 0.022 # m
duesenflaeche     = math.pi * (duesendurchmesser/2)**2 # m^2 unter Annahme einer runden Düse
step = 0.005 # wie genau auflösen? 1 sekunde # TODO ist wahrscheinlich zu ungenau
breakSecond = 1.5

dummy = 1234.234

# matplotlib
x_list = []
twr_list = []
Vrakete_list = []
pressure_list = []

# daten für iterative vorgehensweise
# vars to be changed every iteration
masse       = startmasse # gramm
second      = step
pressure    = initialpressure
Vrakete     = 0 # m/s
luftvolumen = initialLuftvolumen

# powered ascend
# loop for sigma function
while second <= breakSecond and masse>0:
    print("----------Sekunde: {}----------".format(second))
    # iterieren pro sekunde

    # berechnen:
    Vwasser        = (2*pressure/dichte)**0.5 # m/s keine Ahnung, warum man den Durchmesser nicht braucht, siehe auch https://www.physikerboard.de/topic,45753,-wasserstrahlaustrittsgeschwindigkeit-einer-1mm-duese.html
    austrVolumen   = duesenflaeche * Vwasser * step # m^2 * m/s * s = m^3
    austrMasse     = austrVolumen * dichte           # m^3*kg/m^3=kg
    thrust         = austrMasse*Vwasser # kg*m/s = N
    twr            = thrust/(masse*constants.g)
    beschleunigung = thrust/masse*step - constants.g*step # impulsänderung durch Wasseraustritt (+m/s) - impulsänderung durch Gravitation (-m/s)
    Vrakete       += beschleunigung

    # auswerten:                                                                                                                                                              Vrakete            Vwasser            beschleunigung            twr            austrMasse            austrVolumen            masse            pressure
    print("Vrakete: {} m/s,\nVwasser: {} m/s,\nbeschleunigung: {} m/s^2,\nTWR: {},\naustrMasse: {} kg,\naustrVolumen: {} m^3,\nmasse: {} kg,\npressure: {} bar\n".format(round(Vrakete, 2), round(Vwasser, 2), round(beschleunigung, 2), round(twr, 2), round(austrMasse, 2), round(austrVolumen, 5), round(masse, 2), round(pressure/10**5, 2)))
    x_list.append(second)
    twr_list.append(twr)
    Vrakete_list.append(Vrakete)
    pressure_list.append(pressure/10**5)

    # vars für nächsten step bereit machen
    masse       -= austrMasse
    luftvolumen += austrVolumen # die Luft hat nun etwas mehr platz, da Wasser fehlt
    pressure    = initialpressure*initialLuftvolumen/luftvolumen # Pa*m^3/m^3=Pa
    second += step
    second = round(second, 4) # TODO ACHTUNG wenn step kleiner als round gibt es eine endlose schleife

fig, axs = plt.subplots(3)
fig.legend(["TWR", "Vrakete"])
fig.suptitle("Waterrocket data")
axs[0].plot(x_list, twr_list, "tab:green")
axs[0].set_title("TWR")
axs[1].plot(x_list, Vrakete_list, "tab:red")
axs[1].set_title("velocity rocket")
axs[2].plot(x_list, pressure_list, "tab:blue")
axs[2].set_title("pressure")
plt.show()