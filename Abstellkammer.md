# Abstellkammer

Massenstrom: $\frac{dm}{dt} = v_{Str}\rho_WA_D$, wobei $c_W$ wiederum von der Wassermasse in der Rakete abhängt, da diese den Luftinnendruckdruck bestimmt. Ich gehe nämlich davon aus, dass die Menge Luft während das Wasser auströmt gleich bleibt und sich somit der Raum für selbige erhöht, desto mehr Wasser ausstömt. Die Luftmasse berechnet sich zu:
$$m_L = V_L*\frac{p_0*M}{R*T}\tag{1.1}$$
Hierbei ist $M$ die molare Masse mit 0.028949kg/mol für trockene Luft, $R$ die Reynoldszahl mit 8.3145 J/(mol*K) und T die Temperatur mit 20°C, was 293.15K entspricht. $V_L$ ist der Anteil an Luft vom Raketentank ($V_L = V_T-V_W$).  
Damit ist der Luftinnendruck in der Rakete: $$p=\frac{\rho_L*R*T}{M}\tag{1.2}$$
Die Dichte der Luft $\rho_L$ ergibt sich aus dem Quotienten der, wie schon erwähnt konstanten, Masse der Luft $m_L$ und dem nicht (mehr) vom Wasser eingenommenen Volumen $V_L = V_T - V_W = V_T-\frac{m_W}{\rho_W}$. Setzt man dies für $p$ in die umgestellte Bernoulli-Gleichung $v = \sqrt{\frac{2p}{\rho_W}}$ ein, erhält man:
$$v_{Str} = \sqrt{\frac{2(\frac{\frac{m_L}{V_T-m_W/\rho_W}*R*T}{M}-1*10^5)}{\rho_W}}\tag{2}$$
Vom Druck werden 100000 Pa subtrahiert, da für $v_{Str}$ der relative Druck zur Umgebung benötigt wird.
In die Gleichung zum Massenstrom eingesetzt und vereinfacht ergibt sich:
$$\frac{dm_W}{dt}=\frac{\sqrt{2Rm_LT}\rho_WA_D}{\sqrt{V_T-\frac{m_W}{\rho_W}}*\sqrt{\rho_WM}}\tag{3}$$
Nun werden die Veränderlichen $m_W$ und $t$ getrennt und es kann integriert werden. Zur Vereinfachung wird der Term $\sqrt{2Rm_LT}\rho_WA_D$ als $K$ und der Term $\sqrt{\rho_WM}$ als $L$ benannt.
$$\int_{m_s}^m\sqrt{V_T-\frac{m_W}{\rho_W}}dm=\int_0^t\frac{K}{L}dt\tag{4.1}$$
$$\frac{2\rho_W*(\frac{V_T\rho_W-m_s}{\rho_W})^{\frac{3}{2}}}{3}-\frac{2\rho_W*(\frac{V_T\rho_W-m}{\rho_W})^{\frac{3}{2}}}{3}=\frac{Kt}{L}=\frac{\sqrt{2Rm_LT}\rho_WA_Dt}{\sqrt{\rho_WM}}\tag{4.2}$$
Um die Massenabnahme des Wassers über die Zeit $t$ darzustellen muss man nun noch nach $m$ umstellen und erhält:
$$m(t) = -\rho_W \left(\sqrt[3/2]{(V_T-\frac{m_s}{\rho_W})^{\frac{3}{2}}-\frac{2}{3}\frac{Kt}{L\rho_W}}-V_T\right)\tag{5.1}$$
m - m0 ist richtig WICHTIG!!!
