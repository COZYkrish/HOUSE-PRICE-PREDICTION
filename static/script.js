// ============================================================
// House Price Predictor — Frontend Script (Random Forest)
// ============================================================

// Auto-fill location fields when city is selected
async function fillCityData(cityName) {
  const pill = document.getElementById("cityPill");
  const pillText = document.getElementById("cityPillText");

  if (!cityName) {
    pill.style.display = "none";
    return;
  }

  try {
    const resp = await fetch(`/city-info/${encodeURIComponent(cityName)}`);
    const data = await resp.json();
    if (data.error) return;

    document.getElementById("postal_code").value = data.postal_code;
    document.getElementById("latitude").value    = data.latitude;
    document.getElementById("longitude").value   = data.longitude;

    pillText.textContent = `${cityName}  ·  Postal: ${data.postal_code}  ·  Lat: ${data.latitude}  ·  Lon: ${data.longitude}`;
    pill.style.display = "flex";
  } catch (err) {
    console.error("City lookup failed:", err);
  }
}

// Predict price
async function predictPrice() {
  const btn    = document.getElementById("predictBtn");
  const btnTxt = document.getElementById("btnText");
  const result = document.getElementById("resultCard");
  const error  = document.getElementById("errorCard");

  result.style.display = "none";
  error.style.display  = "none";

  // Validate city
  const city = document.getElementById("city_select").value;
  if (!city) {
    showError("Please select a city / area from the Location section.");
    return;
  }

  btn.disabled  = true;
  btnTxt.textContent = "⏳ Running Random Forest...";

  const payload = {
    bedrooms:           getVal("bedrooms"),
    bathrooms:          getVal("bathrooms"),
    living_area:        getVal("living_area"),
    lot_area:           getVal("lot_area"),
    floors:             getVal("floors"),
    waterfront:         getVal("waterfront"),
    views:              getVal("views"),
    condition:          getVal("condition"),
    grade:              getVal("grade"),
    area_excl_basement: getVal("area_excl_basement"),
    basement_area:      getVal("basement_area"),
    built_year:         getVal("built_year"),
    renovation_year:    getVal("renovation_year"),
    postal_code:        getVal("postal_code"),
    latitude:           getVal("latitude"),
    longitude:          getVal("longitude"),
    living_area_renov:  getVal("living_area_renov"),
    lot_area_renov:     getVal("lot_area_renov"),
    schools_nearby:     getVal("schools_nearby"),
    airport_distance:   getVal("airport_distance"),
  };

  // Validate all fields
  for (const [key, val] of Object.entries(payload)) {
    if (val === "" || isNaN(Number(val))) {
      showError(`Please check the value for: "${key.replace(/_/g, " ")}"`);
      resetBtn(btn, btnTxt);
      return;
    }
  }

  try {
    const resp = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });
    const data = await resp.json();

    if (data.error) {
      showError(data.error);
    } else {
      document.getElementById("resultPrice").textContent = data.formatted_price;
      document.getElementById("resultCity").textContent  = "📍 " + city;
      result.style.display = "block";
      result.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  } catch (err) {
    showError("Cannot reach the server. Make sure app.py is running on port 5000.");
  }

  resetBtn(btn, btnTxt);
}

function getVal(id) {
  const el = document.getElementById(id);
  return el ? el.value.trim() : "";
}

function resetBtn(btn, btnTxt) {
  btn.disabled       = false;
  btnTxt.textContent = "🌳 Predict with Random Forest";
}

function showError(msg) {
  const el = document.getElementById("errorCard");
  document.getElementById("errorMsg").textContent = msg;
  el.style.display = "flex";
  el.scrollIntoView({ behavior: "smooth", block: "center" });
}

function resetForm() {
  const defaults = {
    bedrooms: 3, bathrooms: 2, living_area: 1500, lot_area: 5000,
    floors: 1, waterfront: 0, views: 0, condition: 3, grade: 7,
    area_excl_basement: 1200, basement_area: 300,
    built_year: 2000, renovation_year: 0,
    living_area_renov: 1600, lot_area_renov: 5000,
    schools_nearby: 3, airport_distance: 15,
  };
  for (const [id, val] of Object.entries(defaults)) {
    const el = document.getElementById(id);
    if (el) el.value = val;
  }
  document.getElementById("city_select").value = "";
  document.getElementById("cityPill").style.display = "none";
  document.getElementById("resultCard").style.display = "none";
  document.getElementById("errorCard").style.display  = "none";
}
