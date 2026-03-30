const predictBtn = document.getElementById("predictBtn");
const resetBtn = document.getElementById("resetBtn");
const historyDiv = document.getElementById("history");

// Load history
function loadHistory() {
    let history = JSON.parse(localStorage.getItem("sleepHistory")) || [];
    historyDiv.innerHTML = "<h3>📜 History</h3>";

    history.forEach((item, i) => {
        historyDiv.innerHTML += `
        <p>${i+1}. Sleep: ${item.sleep}, Stress: ${item.stress}, Exercise: ${item.exercise} → <b>${item.result}</b></p>
        `;
    });
}

loadHistory();

// Predict
predictBtn.addEventListener("click", async () => {

    const sleep = document.getElementById("sleep").value;
    const stress = document.getElementById("stress").value;
    const exercise = document.getElementById("exercise").value;

    if (!sleep || !stress || !exercise) {
        alert("Fill all fields!");
        return;
    }

    const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            sleep_duration: sleep,
            stress: stress,
            exercise: exercise
        })
    });

    const data = await res.json();
    const result = parseFloat(data.prediction);

    document.getElementById("result").innerText = "Sleep Quality: " + result;

    let msg = "";
    if (result >= 7) msg = "🌟 Excellent sleep!";
    else if (result >= 5) msg = "🙂 Good sleep";
    else if (result >= 3) msg = "⚠️ Poor sleep";
    else msg = "❌ Very bad sleep";

    document.getElementById("message").innerText = msg;

    // Save history
    let history = JSON.parse(localStorage.getItem("sleepHistory")) || [];
    history.push({sleep, stress, exercise, result});
    localStorage.setItem("sleepHistory", JSON.stringify(history));

    loadHistory();
});

// Reset
resetBtn.addEventListener("click", () => {
    document.getElementById("sleep").value = "";
    document.getElementById("stress").value = "";
    document.getElementById("exercise").value = "";
});