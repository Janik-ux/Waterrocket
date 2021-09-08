var heightgraph = null;
var maxspeedgraph = null;

function calcByPressure(volumen, leergewicht, flaecheDues, flaecheRak, winkel) {
    var data = [new Array(), new Array(), new Array()]; // 0: druck, 1: height, 2: maxspeed
    var wasser = 0.3 * volumen;
    var wasserInKubik = wasser * (10 ** -3)
    var startmasse = leergewicht + wasser; // + (0.68*(0.012*volumen)); //TODO hier noch Gewicht der Luft vlt.
    for (var druck = 0; druck <= 15; druck += 0.2) { // here the data is produced
        druckfixed = druck.toFixed(1);
        data[0].push(druckfixed);
        var beschlweg;
        var curdruck = druckfixed;
        nstep = 0.2;
        var gesStrecke = 0;
        var ausgetrWas = 0;
        var localG = 9.81;

        for (n = 0; n <= 30; n += nstep) { // iterative pulling forward time because i'm too stupid to build a formula
            n = parseFloat(n.toFixed(1));
            var curWasser = wasserInKubik - ausgetrWas;
            if (curWasser < 0) {
                ausgschw = 0;
            } else {
                // is the Vout of Water
                ausgschw = ((2 * curdruck) / (1000 * (1 - (flaecheDues / flaecheRak) ** 2 + (1 / winkel - 1) ** 2))) ** 0.5; // J
            }
            // maths go here in step n
            StromProN = nstep * flaecheDues * ausgschw; // Massestrom pro step n brauch ich um zu wissen, wieviel menge ausgestoßen wird in der Zeit
            console.log("strom pro n: " + StromProN);
            ausgetrWas += StromProN;
            vraket = ausgschw / (leergewicht / 1000 + (curWasser)); // keine Ahnung, ob volumen oder wassser
            StreckeProN = (vraket * nstep) - 1 / 2 * localG * (nstep ** 2);
            gesStrecke += StreckeProN;
            console.log("strecke pro n: " + StreckeProN);
            console.log("vraket bei s=" + n + " : " + vraket);
            console.log("ausgwsch bei s=" + n + " : " + ausgschw);
        }
        beschlweg = gesStrecke; // TODO

        data[1].push((beschlweg).toFixed(2)); // + restweg
        // data[2].push(maxgeschw);
        console.log("Gesstrecke: " + gesStrecke);
    }
    return data;
}

function run() {
    var heightgraphctx = document.getElementById("heightgraph");
    var maxspeedgraphctx = document.getElementById("maxspeedgraph");
    // heightgraphctx.height = 50;
    var leergewicht = document.getElementById("leergewicht").valueAsNumber;
    var volumen = document.getElementById("volumen").valueAsNumber;
    var flaecheDues = Math.PI * (document.getElementById("durchmesserDues").valueAsNumber / 2) ** 2;
    var flaecheRak = Math.PI * (document.getElementById("durchmesserRak").valueAsNumber / 2) ** 2;
    var winkel = document.getElementById("winkel").valueAsNumber;
    console.log('============in run=============');
    console.log("Füllvolumen: " + volumen);
    console.log("durchmesser: " + document.getElementById("durchmesserDues").valueAsNumber);
    console.log("fläche: " + flaecheDues);
    console.log("flächeRak: " + flaecheRak);

    var data = calcByPressure(volumen, leergewicht, flaecheDues, flaecheRak, winkel);
    var drucklist = data[0];
    var heightlist = data[1];
    var maxspeedlist = data[2];
    console.log("drucklist: " + drucklist);
    console.log("heightlist: " + heightlist);

    // data = calcByPressure(volumen, leergewicht - (leergewicht * 0.1), flaecheDues, flaecheRak);
    var heightlistminus = data[1];
    var maxspeedminus = data[2];

    // data = calcByPressure(volumen, leergewicht + (leergewicht * 0.1), flaecheDues, flaecheRak);
    var heightlistplus = data[1];
    var maxspeedplus = data[2];

    if (heightgraph != null) {
        heightgraph.destroy();
        heightgraph = null;
    }
    if (maxspeedgraph != null) {
        maxspeedgraph.destroy();
        maxspeedgraph = null;
    }
    heightgraph = new Chart(heightgraphctx, {
        type: 'line',
        data: {
            labels: drucklist,
            datasets: [{
                    label: 'weight like assigned',
                    data: heightlist,
                    fill: true,
                    borderColor: "rgb(62,149,205)",
                    backgroundColor: "rgb(62,149,205,0.1)",
                    borderWidth: 1
                },
                {
                    label: 'wheight - 10%',
                    data: heightlistminus,
                    fill: true,
                    borderColor: "rgb(62,149,205)",
                    backgroundColor: "rgb(62,149,205,0.1)",
                    borderWidth: 0.75
                },
                {
                    label: 'wheight + 10%',
                    data: heightlistplus,
                    fill: true,
                    borderColor: "rgb(62,149,205)",
                    backgroundColor: "rgb(62,149,205,0.1)",
                    borderWidth: 0.75
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'height in a function of pressure'
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'pressure (in bar)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'height'
                    }
                }
            }
        }
    });
    maxspeedgraph = new Chart(maxspeedgraphctx, {
        type: 'line',
        data: {
            labels: drucklist,
            datasets: [{
                    label: 'weight like assigned',
                    data: maxspeedlist,
                    fill: true,
                    borderColor: "rgb(134,191,36)",
                    backgroundColor: "rgb(134,191,36,0.1)",
                    borderWidth: 1
                },
                {
                    label: 'weight - 10%',
                    data: maxspeedminus,
                    fill: true,
                    borderColor: "rgb(134,191,36)",
                    backgroundColor: "rgb(134,191,36,0.1)",
                    borderWidth: 0.75
                },
                {
                    label: 'weight + 10%',
                    data: maxspeedplus,
                    fill: true,
                    borderColor: "rgb(134,191,36)",
                    backgroundColor: "rgb(134,191,36,0.1)",
                    borderWidth: 0.75
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'maximal speed in a function of pressure'
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'pressure (in bar)'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'maximal speed'
                    }
                }
            }
        }
    });
    console.log("flächeRak: " + flaecheRak);
}