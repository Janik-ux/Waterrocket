var heightgraph = null;
var maxspeedgraph = null;

function calcByPressure(volumen, leergewicht, flaeche) {
    var data = [new Array(), new Array(), new Array()]; // 0: druck, 1: height, 2: maxspeed
    var wasser = 0.3 * volumen;
    var startmasse = leergewicht + wasser // + (0.68*(0.012*volumen)); //TODO hier noch Gewicht der Luft vlt.
    for (var druck = 0; druck <= 15; druck += 0.2) { // here the data is produced
        druckfixed = druck.toFixed(1);
        data[0].push(druckfixed);
        if (druckfixed == 0) {
            // to avoid infinity we are passing this by hand
            data[1].push(0);
            data[2].push(0);
            continue;
        }
        var ausgschw = ((2 * (druckfixed * (10 ** 5))) / 1000) ** 0.5; // all assuming we use water
        var maxgeschw = ausgschw * Math.log(startmasse / leergewicht) - ((9.81) * (wasser / (1000 * flaeche * ausgschw))); // before "-" is the acceleration up and beyond its the downacceleration
        var beschlweg = 0.5 * maxgeschw * (wasser * (10 ** -3) / (flaeche * ausgschw));
        var restweg = 0.5 * maxgeschw * (maxgeschw / 9.81);
        // console.log("_______nextturn_______");
        // console.log("ausgschw: " + ausgschw);
        // console.log("maxgeschw: " + maxgeschw);
        // console.log("beschlweg: " + beschlweg);
        // console.log("restweg: " + restweg);
        // console.log("druck: " + druckfixed);
        data[1].push((beschlweg + restweg).toFixed(2));
        data[2].push(maxgeschw);
        // heightlist.push(ausgschw)
        // heightlist.push(maxgeschw)
    }
    return data;
}

function run() {
    var heightgraphctx = document.getElementById("heightgraph");
    var maxspeedgraphctx = document.getElementById("maxspeedgraph");
    // heightgraphctx.height = 50;
    var leergewicht = document.getElementById("leergewicht").valueAsNumber;
    var volumen = document.getElementById("volumen").valueAsNumber;
    var flaeche = Math.PI * (document.getElementById("durchmesser").valueAsNumber / 2) ** 2;
    console.log('============in run=============');
    console.log("Füllvolumen: " + volumen);
    console.log("durchmesser: " + document.getElementById("durchmesser").valueAsNumber);
    console.log("fläche: " + flaeche);

    var data = calcByPressure(volumen, leergewicht, flaeche);
    var drucklist = data[0];
    var heightlist = data[1];
    var maxspeedlist = data[2];
    console.log("drucklist: " + drucklist);
    console.log("heightlist: " + heightlist);

    data = calcByPressure(volumen, leergewicht - (leergewicht * 0.1), flaeche);
    var heightlistminus = data[1];
    var maxspeedminus = data[2];

    data = calcByPressure(volumen, leergewicht + (leergewicht * 0.1), flaeche);
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
}