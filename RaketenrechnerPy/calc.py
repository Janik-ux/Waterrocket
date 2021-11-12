import scipy.constants as constants
import math
# ----inital data----
# not to be changed from code itself
# here configure youir rocket data
startmasse  = 1.745 # kg
leermasse   = 0.445 # kg
dichte      = 1000 # kg/m^3
initialpressure = 15 * 10**5 # Pa
breakSecond = 20
duesendurchmesser = 0.022 # m
duesenflaeche     = math.pi * (duesendurchmesser/2)**2 # m^2 unter Annahme einer runden Düse
step = 0.1 # wie genau auflösen? 1 sekunde # TODO ist wahrscheinlich zu ungenau

# daten für iterative vorgehensweise
# vars to be changed every iteration
masse       = startmasse # gramm
second      = 0
pressure    = initialpressure
Vrakete     = 0 # m/s

# powered ascend
while second <= breakSecond:
    print("----------Sekunde: {}----------".format(second))
    # iterieren pro sekunde
    Vwasser = (2*pressure/dichte) # m/s keine Ahnung, warum man den Durchmesser nicht braucht 
                                  # siehe auch https://www.physikerboard.de/topic,45753,-wasserstrahlaustrittsgeschwindigkeit-einer-1mm-duese.html
    austrMasse = duesenflaeche * Vwasser * step * 1000 # kg weil m^2 * m/s * 1s = m^3, m^3*kg/m^3=kg
    thrust = austrMasse*Vwasser # kg*m/s = N
    twr = thrust/(masse*constants.g)
    Vrakete += thrust/masse*step # impulsänderung durch Wasseraustritt (+m/s)
    Vrakete -= constants.g*step # impulsänderung durch Gravitation (-m/s)
    print("Vrakete: {} m/s,\nTWR: {},\naustrMasse: {} kg,\nmasse: {} kg\n".format(round(Vrakete, 2), round(twr, 2), round(austrMasse, 2), round(masse, 2)))
    masse -= austrMasse
    if masse <= 0:
        break # quickfix normal mit druck regeln, sodass einfach keine austrMasse mehrabgezogen wird.
    second += step
