/*
v1.0.0
(c) 2022 Janik-ux
licensed under MIT license

This program simulates the two dimensional flight of a waterrocket.
*/
var outsidesgraph = null;
var insidesgraph = null;

function reset() {
    data_presets = {
        "m_Struktur": "0.15",
        "V_T":"1", "d_D":"4",
        "A_R":"0.00785",
        "p_P":"6",
        "m_W_s":"0.3",
        "c_w_R":"0.2"
    }
    for (const [key, value] of Object.entries(data_presets)) {
        document.getElementById(key).value = value;
    }
}

function run() {
    h_R_list = calc()
    plot(h_R_list)
}

function calc() {
    // "naturkonstanten" und Umwelteinflüsse
    var R = 8.3145; // J/(mol*kg)
    var M = 0.028949; // kg/mol
    var G = 6.67259 * Math.pow(10, -11); // Gravitationskonstante
    var m_Erde = 5.972 * Math.pow(10, 24); // kg
    var radius_Erde = 6.371000785 * Math.pow(10, 6); // m
    var rho_W = 997; // kg/m^3
    var p_A0 = 1.01325 * Math.pow(10, 5); // Pa Außendruck bei 0m ü NN nach ISA
    var T = 288.15; // K Temp bei 0m nach ISA
    var h_Boden = 100; // m ü NN

    // variable Umwelteinflüsse
    function p_A(h) {
    return p_A0 * (1 - 0.0065 * h / T); // Pa
    }
    function rho_L_A(h) {
    var p;
    p = p_A(h);
    return p * M / (R * T); // kg/m^3
    }
    function g(h) {
    return -(G * m_Erde) / Math.pow(h + radius_Erde, 2); // m/s^2
    }

    // Raketenspezifikationen
    var V_T = document.getElementById("V_T").valueAsNumber / 1000; // L to 
    var m_W_s = document.getElementById("m_W_s").valueAsNumber; // kg
    var m_Struktur = document.getElementById("m_Struktur").valueAsNumber; // kg
    var m_Nutz = 0; // kg
    var p_P = document.getElementById("p_P").valueAsNumber * Math.pow(10, 5); // Pa
    var A_R = document.getElementById("A_R").valueAsNumber; // m^2
    var d_D = document.getElementById("d_D").valueAsNumber; // mm
    var c_w_R = document.getElementById("c_w_R").valueAsNumber;
    var h_start = document.getElementById("h_start").valueAsNumber; // m über h_Boden

    // Einstellungen
    var dt = 0.01;
    var max_t = 20;
    var debug = false;
    var calculate_LW = true;

    // vom Programm berechnete Werte
    var p_0 = p_A(h_start+h_Boden) + p_P; // Pa
    var V_W_s = m_W_s / rho_W; // m^3
    var m_L_s = (V_T - V_W_s) * (p_0 * M / (R * T)); // kg
    var A_D = 1 / 4 * Math.PI * Math.pow(d_D / 1000, 2); // m^2
    var m_R_s = m_Struktur + m_Nutz + m_L_s + m_W_s; // m

    // initialisieren der Speicherstrukturen für die Werte
    var v_str_list = [];
    var t_list = [];
    var V_W_list = [];
    var m_W_list = [];
    var p_L_list = [];
    var m_L_list = [];
    var h_R_list = [];
    var v_R_list = [];
    var a_R_list = [];
    var m_R_list = [];
    var a_R_Luft_list = [];
    var twr_list = [];

    // Über die Berechnung variable Werte
    var h_R = h_start; // Höhe über dem Boden
    var v_R = 0;
    var m_R = m_R_s;
    var V_W = V_W_s;
    var m_L = m_L_s;
    var t = 0;

    while (t < max_t && h_R >= 0) {
        let rho_L = m_L / (V_T - V_W);
        let p_L = Math.round(rho_L * R * T / M, 10);

        if (p_L < p_A(h_R+h_Boden)) {
            console.log(`p_L < p_A (${p_L})`);
            console.log(`Druckausgleich nach ${t} Sekunden.`);
            p_L = p_A(h_R+h_Boden);
            rho_L = p_L * M / (R * T);
            m_L = rho_L * V_T;
        }

        if (calculate_LW) {
            let richtung = v_R > 0 ? -1 : 1;
            var F_Luft = 1 / 2 * rho_L_A(h_R+h_Boden) * A_R * c_w_R * Math.pow(v_R, 2) * richtung; // maybe change to let
            var dv_R_Luft = F_Luft / m_R * dt;
        } else {
            var dv_R_Luft = 0;
        }

        if (V_W > 0) {
            var v_str = Math.pow(2 * (p_L - p_A(h_R+h_Boden)) / rho_W, 0.5);
            var dV_W = v_str * A_D * dt;
            var F_R_str = dV_W * rho_W * v_str;
            var dv_R_str = F_R_str / m_R;
            var dm_L = 0;
        } else {
            var v_str = Math.pow(2 * (p_L - p_A(h_R+h_Boden)) / rho_L, 0.5);
            var dm_L = v_str * A_D * dt * rho_L;
            var F_R_str = dm_L * v_str;
            var dv_R_str = F_R_str / m_R;
            var dV_W = 0;
        }

        var twr = Math.abs(F_R_str) / Math.abs(g(h_R+h_Boden) * dt * m_R);
        var dv_R = dv_R_str + g(h_R+h_Boden) * dt + dv_R_Luft;
        v_R += dv_R;
        h_R += v_R * dt;

        if (debug) {
            console.log(`V_W: ${V_W}`);
            console.log(`m_L: ${m_L}`);
            console.log(`v_str: ${v_str}`);
            console.log(`dV: ${v_str * A_D * dt}`);
            console.log(`rho_L: ${rho_L}`);
            console.log(`p_L: ${p_L}`);
        }

        v_str_list.push(v_str);
        t_list.push(t.toFixed(((dt.toString()).split(".")[1]).length));
        V_W_list.push(V_W);
        p_L_list.push(p_L);
        m_L_list.push(m_L);
        m_W_list.push(V_W*rho_W)
        v_R_list.push(v_R);
        a_R_list.push(dv_R / dt);
        h_R_list.push(h_R);
        m_R_list.push(m_R);
        a_R_Luft_list.push(dv_R_Luft / dt);
        twr_list.push(twr);
        V_W -= dV_W;

        if (V_W < 0) {
            dV_W += V_W;
            console.log(`V_W < 0! (${V_W})`);
            console.log(`Wasser leer nach ${t} Sekunden`);
            V_W = 0;
        }

        m_R -= dV_W * rho_W;
        m_R -= dm_L;
        m_L -= dm_L;
        t += dt;
    }

    console.log(`Total Iterations: ${Math.round(t / dt, 0)}`);
    console.log(Math.max(...h_R_list)) // spread the array into his parts, so max() can better understand it
    return {
        t_list: t_list,
        h_R_list: h_R_list,
        v_R_list: v_R_list,
        a_R_list: a_R_list,
        v_str_list: v_str_list,
        m_R_list: m_R_list,
        m_L_list: m_L_list,
        m_W_list: m_W_list,
        p_L_list: p_L_list

    }
}

function plot(data) {
    var ctx_out = document.getElementById("outsidesgraph").getContext('2d');
    var ctx_in = document.getElementById("insidesgraph").getContext('2d');
    if (outsidesgraph != null) {
        outsidesgraph.destroy();
        outsidesgraph = null;
    }
    if (insidesgraph != null) {
        insidesgraph.destroy();
        insidesgraph = null;
    }
    outsidesgraph = new Chart(ctx_out, {
        type: 'line',
        data: {
            labels: data.t_list,
            datasets: [{
                    label: "Höhe Rakete über Boden",
                    data: data.h_R_list,
                    fill: false,
                    borderColor: "red",
                    borderWidth: 0.75
                },
                {
                    label: "Geschwindigkeit Rakete",
                    data: data.v_R_list,
                    fill: false,
                    borderColor: "blue",
                    borderWidth: 0.75
                },
                {
                    label: "Beschleunigung Rakete",
                    data: data.a_R_list,
                    fill: false,
                    borderColor: "green",
                    borderWidth: 0.75                    
                },
                {
                    label: "v Strahl Rakete",
                    data: data.v_str_list,
                    fill: false,
                    borderColor: "black",
                    borderWidth: 0.75
                }
        ]
        },
        options:{
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'äußere Werte vs time'
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 't in secs'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'm'
                    }
                }
            },
            elements: {
                point:{
                    radius: 0
                }
            }
        } 
    });

    // change unit
    p_L_list = data.p_L_list
    p_L_list.forEach((p, index, arr) => arr[index] = p/Math.pow(10, 5)-1)

    insidesgraph = new Chart(ctx_in, {
        type: 'line',
        data: {
            labels: data.t_list,
            datasets: [{
                    label: "Masse Rakete",
                    data: data.m_R_list,
                    fill: false,
                    borderColor: "red",
                    borderWidth: 0.75
                },
                {
                    label: "Masse Luft in Rakete",
                    data: data.m_L_list,
                    fill: false,
                    borderColor: "blue",
                    borderWidth: 0.75
                },
                {
                    label: "Masse Wasser in Rakete",
                    data: data.m_W_list,
                    fill: false,
                    borderColor: "green",
                    borderWidth: 0.75                    
                },
                {
                    label: "Überdruck in Rakete (bar)",
                    data: p_L_list,
                    fill: false,
                    borderColor: "black",
                    borderWidth: 0.75
                }
        ]
        },
        options:{
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'innere Werte vs time'
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 't in secs'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: ''
                    }
                }
            },
            elements: {
                point:{
                    radius: 0
                }
            }
        } 
    });
}

