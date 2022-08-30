# altes Berechnungsscript vor calc2
# (c) 2021 Janik-ux

import scipy.constants as constants
import math
import matplotlib.pyplot as plt
# ----inital data----
# not to be changed from code itself
# here configure your rocket data
dichte      = 1000 # kg/m^3
wasserfuellanteil = 1/3
luftfuellanteil = 1-wasserfuellanteil
leermasse   = 0 # 0.445 # kg
gesamtvolumen = 4.6 * 10**-3 # L * 10^-3 = m^3
wassermasse = gesamtvolumen*wasserfuellanteil*dichte
startmasse = wassermasse + leermasse
initialLuftvolumen = gesamtvolumen*luftfuellanteil
initialwasservolumen = gesamtvolumen*wasserfuellanteil
initialpressure = 15 * 10**5 # Pa
initialpressure = initialpressure + 1 # weg en atmosphäre
duesendurchmesser = 0.0022 # m # default 0.022
duesenflaeche     = math.pi * (duesendurchmesser/2)**2 # m^2 unter Annahme einer runden Düse
step = 0.005 # wie genau auflösen? # TODO ACHTUNG wenn step kleiner als round gibt es eine endlose schleife
breakSecond = 0.5

dummy = 1234.234 # for debugging

# matplotlib
x_list = []
twr_list = []
Vrakete_list = []
pressure_list = []
masse_list = []

# daten für iterative vorgehensweise
# vars to be changed every iteration
masse       = startmasse # gramm
second      = step
pressure    = initialpressure
Vrakete     = 0 # m/s
luftvolumen = initialLuftvolumen
print("Luftvolumen: " + str(luftvolumen))
wasservolumen = initialwasservolumen
print("Wasservolumen: " + str(wasservolumen))
Strecke = 0

# powered ascend
# loop for sum function
while second <= breakSecond and masse>=0:
    # iterieren pro sekunde

    # berechnen:
    Vwasser        = (2*pressure/dichte)**0.5 # m/s keine Ahnung, warum man den Durchmesser nicht braucht, siehe auch https://www.physikerboard.de/topic,45753,-wasserstrahlaustrittsgeschwindigkeit-einer-1mm-duese.html
    austrVolumen   = duesenflaeche * Vwasser * step # m^2 * m/s * s = m^3
    austrMasse     = austrVolumen * dichte           # m^3*kg/m^3=kg
    thrust         = austrMasse*Vwasser # kg*m/s = N
    twr            = thrust/(masse*constants.g)
    beschleunigung = thrust/masse*step - constants.g*step # impulsänderung durch Wasseraustritt (+m/s) - impulsänderung durch Gravitation (-m/s)
    Vrakete       -= beschleunigung
    Strecke       += Vrakete*step

    # auswerten:                                                                                                                                                              Vrakete            Vwasser            beschleunigung            twr            austrMasse            austrVolumen            masse            pressure
    print("----------Sekunde: {}----------".format(second))
    print("Vrakete: {} m/s,\nVwasser: {} m/s,\nbeschleunigung: {} m/s^2,\nbeschleunigung ohne g: {} m/s^2,\nTWR: {},\naustrMasse: {} kg,\naustrVolumen: {} m^3,\nmasse: {} kg,\npressure: {} bar,\nluftvolumen: {} m^3,\nwasservolumen: {} m^3\n".format(round(Vrakete, 2), round(Vwasser, 2), round(beschleunigung, 2), round(beschleunigung+constants.g*step, 7), round(twr, 7), round(austrMasse, 2), round(austrVolumen, 5), round(masse, 2), round(pressure/10**5, 2), round(luftvolumen, 5), round(wasservolumen, 5)))

    # break
    x_list.append(second)
    twr_list.append(twr)
    Vrakete_list.append(Vrakete)
    pressure_list.append(pressure/10**5)
    masse_list.append(masse)

    # vars für nächsten step bereit machen
    masse       -= austrMasse
    luftvolumen += austrVolumen # die Luft hat nun etwas mehr platz, da Wasser fehlt
    wasservolumen -= austrVolumen
    # pressure    = initialpressure*initialLuftvolumen/luftvolumen # Pa*m^3/m^3=Pa
    pressure = 1*gesamtvolumen/luftvolumen
    second += step
    second = round(second, 4) # TODO ACHTUNG wenn step kleiner als round gibt es eine endlose schleife

fig, axs = plt.subplots(4)
fig.legend(["TWR", "Vrakete"])
fig.suptitle("Waterrocket data")
axs[0].plot(x_list, twr_list, "tab:green")
axs[0].set_title("TWR")
axs[1].plot(x_list, Vrakete_list, "tab:red")
axs[1].set_title("velocity")
axs[2].plot(x_list, pressure_list, "tab:blue")
axs[2].set_title("pressure")
axs[3].plot(x_list, masse_list, "tab:pink")
axs[3].set_title("masse")
plt.show()
print(Strecke)
print(gesamtvolumen)
