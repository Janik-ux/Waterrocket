# Berechnungen rund um die Wasserrakete

## Mathematischer Ansatz

### Strecke $s_{Rakete}$

Die Strecke der Rakete hängt von folgenden Faktoren ab:

#### konstant

* Dichte des Ausströmmediums, in unserem Fall Wasser $\rho_{Wasser}$
* entgegengerichtete Beschleunigung, wie zum Beispiel die Erde
* Düsendurchmesser

#### variabel

* Füllanteil von Wasser bezogen auf die Gesamtmenge
* Masse $m$ der Rakete bestehend aus
  * Leermasse  (konstant)
  * Wassermasse (geteilt durch die Dichte ergibt das Volumen $V_{wasser}$) abhängig vom Füllanteil
  * Luftmasse (erstmal vernachlässigt)
* Überdruck in der Rakete
<!-- TODO Luftwiderstand gehört auch mit dazu -->

### Beschleunigung $a_{Rakete}(t)$

Die Beschleunigung $a_{Rakete}(t)$ ergibt sich aus dem 3. Newtonschen Gesetz: $\vec{F}_{A\rightarrow{B}} = -\vec{F}_{B\rightarrow{A}}$, da die Rakete mit dem Rückstoßprinzip arbeitet.
Laut dem 2. Newtonschen Gesetz ist die Kraft gleich der Masse mal der Beschleunigung ($F = ma$). Daher kann man $\vec{F}$ auch als $m*a$ schreiben. Dies können wir nun leicht auf unsere Rakete anwenden: $a_{Rakete}*m_{Rakete} = -a_{Wasser}*m_{Wasser}$. Stellen wir dies nach $a_{Rakete}$ um, so ergibt sich: $$a_{Rakete} = -\frac{a_{Wasser}*m_{Wasseraus}}{m_{Rakete}}\tag{1}$$

1. Um $a_{Wasser}$ zu berechnen, benötigt man die Bernoulli Druckgleichung des ruhenden Sytems ohne Berücksichtigung von Verlusten: $p+\rho*g*z+\frac{\rho}{2}*c^2$. Lässt man den geodätischen Druck $\rho*g*z$ weg, und stellt nach der Geschwindigkeit $c$ um, so erhält man: $$c = \sqrt{\frac{2*p}{\rho_{Wasser}}}=v_{Wasser}\tag{2}$$ wobei $c$ die Strömungsgeschwindigkeit $v_{Wasser}$ beschreibt.

2. Mithilfe dieser Strömungsgeschwindigkeit und den oben gegebenen Faktoren können wir auch noch die zweite zur Berechnung der Beschleunigung benötigte Variable $m_{Wasseraus}$ berechnen. Die Masse $m$ eines Körpers ist gleich dem Produkt von Volumen und Dichte desselben ($m =  \rho * V$). Da $\rho$ schon oben gegeben ist, benötigen wir noch das Volumen $V$. Dies kann man berechnen, in dem man sich das ausgestoßene Wasser als einen Zylinder vorstellt. Die Grundfläche des Zylinders entspricht der Fläche der Düse, also aus unseren gegebenen Faktoren berechenbar, und die Höhe der Entfernung, die das Wasser mit der Austrittsgeschwindigkeit $a_{Wasser}$ in einer Zeit $\Delta t=t_{start}-t_{end}$ zurück gelegt hat. Also ergibt sich:
$$m_{Wasseraus}=\rho_{Wasser}*(A_{Düse}*a_{Wasser}*\Delta t)\tag{3}$$

3. Die dritte Variable ist $m_{Rakete}$, sie besteht aus dem Volumen des Wassers mal seiner Dichte plus dem Leergewicht der Rakete. ($m_{Rakete} = V_{Wasser} * \rho_{Wasser} + m_{Raketeleer}$)

Setzt man dies zusammen, so ergibt sich:

$$a_{Rakete} = -\frac{(\sqrt{\frac{2*p}{\rho_{Wasser}}})*(\rho_{Wasser}*A_{Düse}*\sqrt{\frac{2*p}{\rho_{Wasser}}}*\Delta t)}{V_{Wasser}*\rho_{Wasser} + m_{Raketeleer}}\tag{4}$$

Nun kürzen wir $\rho_{Wasser}$ weg, fassen $\sqrt{\frac{2*p}{\rho_{Wasser}}}*\sqrt{\frac{2*p}{\rho_{Wasser}}}$ zu $(\sqrt{\frac{2*p}{\rho_{Wasser}}})^2=\frac{2*p}{\rho_{Wasser}}$ zusammen und erhalten:

$$a_{Rakete}=-\frac{\frac{2*p}{\rho_{Wasser}}*(A_{Düse}*\Delta t)}{V_{Wasser} + m_{Raketeleer}}-g\tag{5}$$

Leider sind $p$ und $V_{wasser}$ nun variabel über die Zeit $t$, was bedeutet, dass wir für die Beschleunigung $a_{Rakete}(t)$ zur Zeit $t$ die Parameter $p(t)$ und $V_{Wasser}(t)$ haben.

* $p(t)$ hängt vom  Wasservolumen $V_{Wasser}(t)$ ab. Aus dem Gesetz von [Boyle-Mariotte](https://de.wikipedia.org/wiki/Thermische_Zustandsgleichung_idealer_Gase#Gesetz_von_Boyle-Mariotte) folgt, dass das Produkt aus einem Druck und seinem Volumen gleich dem Produkt aus einem zweiten Druck und seinem Volumen ist ($p_1*V_1=p_2*V_2$). Dies können wir auf unsere Rakete wie folgt anwenden: $p(t)=\frac{p_{start}*V_{start}}{V_{Wasser}(t)}$

* $V_{Wasser}(t)=\frac{p_{start}*V_{start}}{p(t)}$ wie leicht ersichtlich ist. Dies ist eine Differentialgleichung, wenn man nämlich $p(t)$ in $V_{Wasser}(t)$ einsetzt: $$V_{Wasser}(t)=\frac{p_{start}*V_{start}}{\frac{p_{start}*V_{start}}{V_{Wasser}(t)}} = \frac{p_{start}*V_{start}*V_{Wasser}(t)}{p_{start}*V_{start}}\tag{6}$$

Differenzieren: $$\frac{dV}{dt}=\frac{p_{start}*V_{start}*V}{p_{start}*V_{start}}=V\tag{7}$$

Die Gleichung ist separabel und man kann die Variablen trennen:

$$\int\frac{1}{V} dV=\int dt$$

$$\ln(|V|)+C=t+C$$

umgestellt:

$$V_{Wasser}(t)=e^{t+C}-C\tag{8}$$

>Gedanke:
>
>Wenn der Anteil des Luftvolumens 100% ist, muss der (über-) Druck null bar betragen.

### Geschwindigkeit $v_{Rakete}$

So ergibt sich nun die Geschwindigkeit $v_{Rakete}$ aus der gleichmäßig beschleunigten Bewegung als $v_{Rakete}(t) =\int a_{Rakete}(t) = a_{Rakete}*t + v_{0_{Rakete}}$ nach der Zeit $t$.

Allerdings haben wir bei der Wasserrakete eine ungleichmäßig beschleunigte Bewegung vorliegen, da sich der innere Druck und die Masse der Rakete über die Zeit $t$ ändern.

## programmatischer Ansatz
$$a_{Rakete}(t) = $$
$$v_{Rakete}=\sum_{k=0}^n a(t) $$
