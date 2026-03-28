document.getElementById('predict-form')
  .addEventListener('submit', async (e) => {

    e.preventDefault();

    // Show loading
    document.getElementById('result-panel').classList.remove('hidden');
    document.getElementById('loading-state').classList.remove('hidden');
    document.getElementById('result-content').classList.add('hidden');

    try {
      // Step 1: Get distance
      const distRes = await fetch('/api/distance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin: document.getElementById('restaurant').value,
          destination: document.getElementById('delivery').value
        })
      });

      const distData = await distRes.json();

      // Step 2: Get prediction
      const predRes = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          distance_km: distData.distance_km,
          prep_time: document.getElementById('prep-time').value,

          // 🔥 NEW FIELDS
          traffic: document.getElementById('traffic').value,
          weather: document.getElementById('weather').value,
          vehicle: document.getElementById('vehicle').value,
          time_of_day: document.getElementById('time_of_day').value
        })
      });

      const data = await predRes.json();

      // Hide loading
      document.getElementById('loading-state').classList.add('hidden');
      document.getElementById('result-content').classList.remove('hidden');

      // Show results
      document.getElementById('res-time').textContent =
        data.total_minutes + " mins";

      document.getElementById('res-range').textContent =
        `Range: ${data.range_low} to ${data.range_high} mins`;

    } catch (error) {
      alert("Something went wrong!");
      console.error(error);
    }
});