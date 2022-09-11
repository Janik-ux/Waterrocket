# Berechnungen rund um die Wasserrakete

## 1 Apoapsishöhe bei interner Beschleunnigung / Flugcharakteristika

Berechnung der verschiedenen wichtigen Werte der durch austretendes Wasser beschleunigten Rakete. Hierbei spielen Triebwerksdruck, Luftwiderrstand und Erdanziehung die größte Rolle.

### 1.1 Mathematischer Ansatz

Impuls des Beobachtersystems:
$$I_{Ges} = 0 = I_R + I_{Str}$$
Der Impuls der Rakete ist positiv, der Impuls des Strahls, durch die Geschwindigkeit entegegen der Rakete, bzw. nach unten, negativ.

Impulsänderung der Rakete:

$\Delta I_R = -\Delta I_{str}$  
$\rightarrow m_R*\Delta v_R = -\Delta m_{Str}*w_{Str}$  
$\Rightarrow (m_R(t) - \Delta m_{Str})*$  
$I_{Str}(t) = m_{Str}(t) + v_{Str}$

Effektive Austrittsgeschwindigkeit, sozusagen, auf das System Rakete bezogen: $w_e(t) = v_{Str}(t) - v_R(t)$.

$dv_R = -w_e(t)\frac{dm_R}{m_R(t)}$

| Name | Beschreibung | Einheit | Veränderung |
| - | - | - | - |
| $m_{Struktur}$ | Masse der Tanks und Düse usw. | kg | konstant |  
| $m_{NL}$       | Masse der Nutzlast(in meinem Fall 0kg) | kg | konstant |
| $m_W$ | Masse des Wassers | kg | variabel |
| $A_D$ | Fläche der Düse, durch die das Wasser gelangt | m² | konstant |
| $p_0$ | Initialer absoluter Druck in der Flasche | Pa | konstant |
| $m_0$ | Startmasse: $m_{Struktur} + m_W + m_{NL}$ | kg | konstant |
| $m_L$ | Masse der Luft: $V_L*\frac{p_0*M}{R*T}$ | kg | konstant |
| $c_W$ | Austrittsgeschwindigkeit Wasser | m/s | variabel |
| $V_T$   | Volumen des Drucktanks | m³ | konstant |
| $V_W$   | Volumen Wasser: $m_W/\rho_W$ | m³ | variabel |
| $\rho_W$ | Dichte des Wassers: 0.998 | kg/m³ | konstant |
| $\rho_L$ | Dichte der Luft | kg/m³ | variabel |
| $p_A$ | Umgebungsdruck 10^5 | Pa | konstant |
<!-- Düsenkoeffizienten? -->

Volumenstrom: $\frac{dV_W}{dt} = v_{Str}A_D$, wobei $v_{Str}$ wiederum von dem Wasservolumen in der Rakete abhängt, da dieses den Luftinnendruck bestimmt. Ich gehe nämlich davon aus, dass die Menge Luft während das Wasser ausströmt gleich bleibt und sich somit der Raum für selbige erhöht.

Der Luftinnendruck in der Rakete ist:

$$p=\frac{\rho_L*R*T}{M}\tag{1.1.1}$$

Hierbei ist $M$ die molare Masse mit 0.028949kg/mol für trockene Luft, $R$ die Reynoldszahl mit 8.3145 J/(mol*K) und T die Temperatur mit 293.15K, was  20°C entspricht.
Die Dichte der Luft $\rho_L$ ergibt sich aus dem Quotienten der, wie schon erwähnt konstanten, Masse der Luft $m_L$ und dem nicht (mehr) vom Wasser eingenommenen Volumen $V_L = V_T - V_W$. Setzt man dies für $p$ in die umgestellte Bernoulli-Gleichung $v = \sqrt{\frac{2p}{\rho_W}}$ ein, erhält man:
$$v_{Str} = \sqrt{\frac{2(\frac{\frac{m_L}{V_T-V_W}*R*T}{M}-p_A)}{\rho_W}}\tag{1.1.2}$$
Vom Druck wird $p_A$ subtrahiert, da für $v_{Str}$ der relative Druck zur Umgebung benötigt wird. Der Geschwindigkeitsbeiwert wurde als 1 angenommen.
In die Gleichung zum Volumenstrom eingesetzt und mit $k=\frac{m_LRT}{M}$ vereinfacht ergibt sich:
$$\frac{dV_W}{dt}=\frac{\sqrt{2}\sqrt{\frac{1}{V_T-V_W}k-p_A}A_D}{\sqrt{\rho_W}} \tag{1.1.3}$$
Nun werden die Veränderlichen $m_W$ und $t$ getrennt und es kann integriert werden.
$$\int\frac{1}{\sqrt{\frac{1}{V_T-V_W}k-p_A}}dV_W=\int\frac{\sqrt{2}A_D}{\sqrt{\rho_W}}dt\tag{1.1.4}$$

## 2 Apoapsishöhe ohne interne Beschleunigung

Man könnte es auch als Berechnung der Freiflugphase bezeichnen. Hier wird die Düse also als ausgeschaltet betrachtet. Es werden nur Luftwiderstand und Erdanziehung betrachtet.  
Wenn der Luftwiderstand, bzw. die Geschwindigkeit der Rakete Null ist, muss die Rakete an der Apoapsis sein.  Die Beschleunigung ergibt sich zu:
$$v'=\frac{dv}{dt}=\frac{kv^2}{m}+g\tag{2.1.1}$$
$$v'm-kv^2=gm$$
Hier stellen $m$ die Masse der Rakete, $v$ die Geschwindigkeit und $g$ die Erdbeschleunigung dar. In $k$ wurden die Unveränderlichen des Luftwiderstands nach Newton der Einfachheit halber zu $\frac{1}{2}Ac_w\rho=k$ zusammengefasst. Es wird mit $m$ und $dt$ multipliziert und dann durch $(kv^2+gm)$ bzw. $m$ geteilt und man erhält die separierte Differentialgleichung:
$$\int \frac{1}{(kv^2+gm)}dv=\int \frac{1}{m}dt\tag{2.1.2}$$
Durch Integrieren erhält man:
$$\frac{\arctan\left(\frac{kv}{\sqrt{gkm}}\right)}{\sqrt{gkm}}+C=\frac{t}{m}\tag{2.1.3}$$
Nun wird die Gleichung Null gesetzt, sodass sich die Zeit, nach der die Rakete ihren höchsten Punkt erreicht hat, zu
$$t=\frac{\arctan\left(\frac{kv}{\sqrt{gkm}}\right)*m}{\sqrt{gkm}}+C*m$$
ergibt.  
Nach $v$ umstellen und ein weiteres Mal integrieren führt zur Weg-Zeit-Gleichung, in die das eben ermittelte t eingesett werden kann, sodass man die Höhe erhält:
$$v=\frac{\tan\left(\frac{t\sqrt{gkm}}{m}-C\sqrt{gkm}\right)*\sqrt{gkm}}{k}\tag{2.1.4}$$
