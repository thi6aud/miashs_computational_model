// --- Étape 1 : Vérifions que tout fonctionne --- //

// On attend que la page soit complètement chargée avant d’exécuter du JS
document.addEventListener("DOMContentLoaded", () => {
  console.log("Page fully loaded and parsed");
});

function startTest() {
  console.log("Starting the test...");

  const bg = document.querySelector(".bg-image");
  const container = document.querySelector(".container");

  // Lance le fondu de l'image de fond (vers le blanc du body)
  if (bg) bg.style.opacity = "0";

  // Après le fondu, on passe au fond blanc et on affiche la zone de test
  setTimeout(() => {
    container.style.color = "black";
    container.innerHTML = "";

    const testArea = document.createElement("div");
    testArea.classList.add("test-area");
    testArea.textContent = "Mot cible";
    testArea.style.fontSize = "2em";
    testArea.style.textAlign = "center";
    container.appendChild(testArea);
  }, 1500); // même durée que la transition CSS
}
