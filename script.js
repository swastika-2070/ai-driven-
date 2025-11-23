async function fetchLiveData() {
  try {
    const response = await fetch("/api/live");
    const data = await response.json();

    document.getElementById("activeThreats").textContent = data.active_threats;
    document.getElementById("highRisk").textContent = data.high_risk_users;
    document.getElementById("avgScore").textContent = data.avg_score.toFixed(2);
  } catch (err) {
    console.error("Error fetching data:", err);
  }
}

setInterval(fetchLiveData, 10000); // refresh every 10 seconds
fetchLiveData(); // initial load
