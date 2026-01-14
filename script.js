let mots = [];
let motCible = "";

// Fonction pour mélanger un tableau (Fisher-Yates shuffle)
function shuffleArray(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

fetch("stimuli_website.json")
  .then(response => response.json())
  .then(data => {
    // Les mots sont maintenant des objets {mot: "...", est_reel: true/false}
    mots = shuffleArray(data.mots_affiches);
    motCible = data.mot_cible;
    console.log("Stimuli chargés et mélangés :", mots);
  });

// --- Étape 1 : Vérifions que tout fonctionne --- //

// On attend que la page soit complètement chargée avant d’exécuter du JS
document.addEventListener("DOMContentLoaded", () => {
  console.log("Page fully loaded and parsed");
});

// --- Helpers pour le déroulé du test --- //
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function waitForStimuli() {
  return new Promise((resolve) => {
    if (mots && mots.length > 0 && motCible) {
      resolve();
      return;
    }
    const check = setInterval(() => {
      if (mots && mots.length > 0 && motCible) {
        clearInterval(check);
        resolve();
      }
    }, 100);
  });
}

async function showCountdown(el, seq = [3, 2, 1], stepMs = 1000) {
  for (const n of seq) {
    el.textContent = String(n);
    await sleep(stepMs);
  }
}

function waitForKey(allowedKeys = ["f", "j"]) {
  return new Promise((resolve) => {
    const handler = (e) => {
      const key = (e.key || "").toLowerCase();
      if (allowedKeys.includes(key)) {
        window.removeEventListener("keydown", handler);
        resolve(key);
      }
    };
    window.addEventListener("keydown", handler);
  });
}

async function startTest() {
  console.log("Starting the test...");

  const bg = document.querySelector(".bg-image");
  const container = document.querySelector(".container");
  if (!container) {
    console.error("Container introuvable");
    return;
  }

  // Lance le fondu de l'image de fond (vers le blanc du body)
  if (bg) bg.style.opacity = "0";

  // Attendre la fin du fondu (même durée que la transition CSS)
  await sleep(1500);

  // Prépare la zone d'affichage
  container.style.color = "black";
  container.innerHTML = "";

  // S'assurer que les stimuli sont chargés
  await waitForStimuli();

  const testArea = document.createElement("div");
  testArea.classList.add("test-area");
  testArea.style.fontSize = "2.5em";
  testArea.style.textAlign = "center";
  testArea.style.marginTop = "20vh";
  container.appendChild(testArea);

  // Affiche le mot cible
  testArea.textContent = `Le mot cible est : ${motCible}`;
  await sleep(2000);

  // Compte à rebours 3,2,1
  await showCountdown(testArea, [3, 2, 1], 1000);

  const resultats = [];

  // Afficher les mots un par un, attendre bonne réponse
  let index = 0;
  while (index < mots.length) {
    const motObj = mots[index];
    const motTexte = motObj.mot;
    const estMotCible = (motTexte.toLowerCase() === motCible.toLowerCase());
    const similarite = motObj.similarite;
    
    testArea.textContent = motTexte;
    testArea.style.color = "black";
    testArea.style.animation = "none";

    const t0 = performance.now(); // début chrono
    let reponseCorrecte = false;
    let tentatives = 0;
    
    while (!reponseCorrecte) {
      const key = await waitForKey(["f", "j"]);
      tentatives++;
      
      // f = c'est le mot cible, j = ce n'est PAS le mot cible
      const reponseUtilisateur = (key === "f");
      
      if (reponseUtilisateur === estMotCible) {
        // Bonne réponse
        reponseCorrecte = true;
        const t1 = performance.now();
        const tempsReaction = Math.round(t1 - t0);
        resultats.push({ mot: motTexte, touche: key, tempsReaction, tentatives, similarite });
      } else {
        // Mauvaise réponse : animation tremblement + rouge
        testArea.style.color = "red";
        testArea.style.animation = "shake 0.5s";
        await sleep(500);
        testArea.style.animation = "none";
        testArea.style.color = "black";
      }
    }
    
    index += 1;
  }

  // Fin du test
  testArea.textContent = "Fin du test";

  // --- Export CSV --- //
  const csvContent =
    "mot,touche,tempsReaction(ms),tentatives,similarite\n" +
    resultats.map(r => `${r.mot},${r.touche},${r.tempsReaction},${r.tentatives},${r.similarite}`).join("\n");

  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const lien = document.createElement("a");
  lien.href = url;
  lien.download = "resultats_humain.csv";
  lien.textContent = "📥 Télécharger les résultats (CSV)";
  lien.style.display = "block";
  lien.style.marginTop = "2em";
  lien.style.textAlign = "center";
  container.appendChild(lien);

  // --- Bouton pour afficher les graphiques --- //
  const boutonGraphiques = document.createElement("button");
  boutonGraphiques.textContent = "Afficher les graphiques";
  boutonGraphiques.style.display = "block";
  boutonGraphiques.style.margin = "2em auto";
  boutonGraphiques.style.padding = "0.5em 1em";
  boutonGraphiques.style.cursor = "pointer";
  // Enhanced visual style for better visibility
  boutonGraphiques.style.background = "#007BFF";
  boutonGraphiques.style.color = "white";
  boutonGraphiques.style.border = "none";
  boutonGraphiques.style.borderRadius = "6px";
  container.appendChild(boutonGraphiques);
  boutonGraphiques.scrollIntoView({ behavior: "smooth" });

  function openChartInWindow(title, chartConfig) {
    const chartWin = window.open('', title, 'width=800,height=600');
    chartWin.document.write('<html><head><title>' + title + '</title><script src="https://cdn.jsdelivr.net/npm/chart.js"></script></head><body><canvas id="chartCanvas"></canvas></body></html>');
    chartWin.document.close();
    chartWin.onload = () => {
      const ctx = chartWin.document.getElementById('chartCanvas').getContext('2d');
      new chartWin.Chart(ctx, chartConfig);
    };
  }

  let chartsLoaded = false;

  boutonGraphiques.addEventListener("click", () => {
    if (chartsLoaded) return;
    chartsLoaded = true;

    function createCharts() {
      // Utiliser les vraies similarités des résultats
      const similarites = resultats.map(r => r.similarite);
      const frequences = resultats.map(r => Math.random() * 700); // TODO: ajouter vraies fréquences

      const temps = resultats.map(r => r.tempsReaction);

      // --- Fonction de régression linéaire simple ---
      function regressionLineaire(x, y) {
        const n = x.length;
        const meanX = x.reduce((a, b) => a + b, 0) / n;
        const meanY = y.reduce((a, b) => a + b, 0) / n;
        const num = x.map((xi, i) => (xi - meanX) * (y[i] - meanY)).reduce((a, b) => a + b, 0);
        const den = x.map(xi => (xi - meanX) ** 2).reduce((a, b) => a + b, 0);
        const slope = num / den;
        const intercept = meanY - slope * meanX;
        const yFit = x.map(xi => slope * xi + intercept);
        return { yFit, slope, intercept };
      }

      const regFreq = regressionLineaire(frequences, temps);
      const regSim = regressionLineaire(similarites, temps);

      // --- Préparer deux fenêtres dès le clic (pour éviter le blocage popup) ---
      const freqWin = window.open('', 'Relation entre fréquence et TR', 'width=800,height=600');
      const simWin = window.open('', 'Relation entre similarité et TR', 'width=800,height=600');

      // Charger Chart.js dans chaque fenêtre
      const baseHTML = `
        <html>
          <head>
            <title>Graphique</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
          </head>
          <body style="margin:20px; font-family:sans-serif;">
            <canvas id="chartCanvas" width="700" height="500"></canvas>
          </body>
        </html>
      `;

      freqWin.name = "freqWin";
      freqWin.document.write(baseHTML);
      simWin.name = "simWin";
      simWin.document.write(baseHTML);
      freqWin.document.close();
      simWin.document.close();

      freqWin.focus();
      simWin.focus();

      // Tracer dans chaque fenêtre une fois Chart.js chargé
      freqWin.onload = () => {
        const ctx = freqWin.document.getElementById("chartCanvas").getContext("2d");
        new freqWin.Chart(ctx, {
          type: "scatter",
          data: {
            datasets: [
              {
                label: "Mots",
                data: frequences.map((x, i) => ({ x, y: temps[i] })),
                backgroundColor: "blue",
              },
              {
                label: "Régression linéaire",
                type: "line",
                data: frequences.map((x, i) => ({ x, y: regFreq.yFit[i] })),
                borderColor: "black",
                borderDash: [5, 5],
                fill: false
              }
            ]
          },
          options: {
            plugins: {
              title: { display: true, text: "Relation entre fréquence et TR" }
            },
            scales: {
              x: { title: { display: true, text: "Fréquence (freqlivres)" } },
              y: { title: { display: true, text: "Temps de réaction (ms)" } }
            }
          }
        });
      };

      simWin.onload = () => {
        const pointsSim = similarites.map((x, i) => ({ x, y: temps[i], yFit: regSim.yFit[i] }))
                                 .sort((a, b) => a.x - b.x);
        const ctx = simWin.document.getElementById("chartCanvas").getContext("2d");
        new simWin.Chart(ctx, {
          type: "scatter",
          data: {
            datasets: [
              {
                label: "Mots",
                data: pointsSim.map(p => ({ x: p.x, y: p.y })),
                backgroundColor: "blue",
              },
              {
                label: "Régression linéaire",
                type: "line",
                data: pointsSim.map(p => ({ x: p.x, y: p.yFit })),
                borderColor: "black",
                borderDash: [5, 5],
                fill: false
              }
            ]
          },
          options: {
            plugins: {
              title: { display: true, text: "Relation entre similarité et TR" }
            },
            scales: {
              x: { title: { display: true, text: "Similarité orthographique" } },
              y: { title: { display: true, text: "Temps de réaction (ms)" } }
            }
          }
        });
      };
    }
    if (typeof Chart === "undefined") {
      const chartScript = document.createElement("script");
      chartScript.src = "https://cdn.jsdelivr.net/npm/chart.js";
      chartScript.onload = () => {
        createCharts();
      };
      document.head.appendChild(chartScript);
    } else {
      createCharts();
    }
  });
}
