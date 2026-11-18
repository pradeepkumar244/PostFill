/* PLI premium calculator. Runs entirely in the browser; nothing is sent to the server. */
(function (root) {
  "use strict";

  function options(rates, age) {
    var row = rates[String(age)];
    if (!row) return [];
    return Object.keys(row).map(Number).sort(function (a, b) { return a - b; })
      .map(function (m) { return { maturity: m, term: m - age, rate: row[m] }; });
  }

  // Monthly premium = rate per Rs 1,000 x (sum assured / 1,000). Integer paise maths avoids
  // floating-point drift.
  function calc(rates, age, maturity, sumAssured, bonusRate) {
    var row = rates[String(age)];
    if (!row || row[String(maturity)] === undefined) return null;
    if (!Number.isInteger(sumAssured) || sumAssured <= 0 || sumAssured % 1000 !== 0) return null;
    var term = maturity - age;
    var paise = Math.round(row[String(maturity)] * 100) * (sumAssured / 1000);
    var res = {
      rate: row[String(maturity)],
      term: term,
      monthly: paise / 100,
      yearly: (paise * 12) / 100,
      total: (paise * 12 * term) / 100
    };
    // Same as the sheet: bonus = (sum assured / 1000) x bonus rate x term; maturity = sum assured + bonus
    if (typeof bonusRate === "number" && bonusRate >= 0) {
      res.bonus = Math.round((sumAssured / 1000) * bonusRate * term * 100) / 100;
      res.maturityAmount = sumAssured + res.bonus;
    }
    return res;
  }

  var api = { options: options, calc: calc };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
  root.PLI = api;

  if (typeof document === "undefined") return;

  document.addEventListener("DOMContentLoaded", function () {
    var dataEl = document.getElementById("pli-data");
    if (!dataEl) return;
    var rates = JSON.parse(dataEl.textContent);
    var ageEl = document.getElementById("pli-age"), matEl = document.getElementById("pli-mat"),
        saEl = document.getElementById("pli-sa"), bonusEl = document.getElementById("pli-bonus"), err = document.getElementById("pli-err"),
        out = document.getElementById("pli-out");
    var minAge = Number(ageEl.min), maxAge = Number(ageEl.max);

    function inr(n) {
      return "\u20B9" + n.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    function show(msg) { err.textContent = msg; err.style.display = msg ? "block" : "none"; }

    function fillMaturity() {
      var age = parseInt(ageEl.value, 10), prev = matEl.value;
      matEl.innerHTML = "";
      var opts = (age >= minAge && age <= maxAge) ? options(rates, age) : [];
      if (!opts.length) {
        matEl.innerHTML = '<option value="">Enter a valid age first</option>';
        return;
      }
      opts.forEach(function (o) {
        var el = document.createElement("option");
        el.value = o.maturity;
        el.textContent = "Age " + o.maturity + " (" + o.term + " years)";
        matEl.appendChild(el);
      });
      if (prev && matEl.querySelector('option[value="' + prev + '"]')) matEl.value = prev;
    }

    function update() {
      var age = parseInt(ageEl.value, 10), mat = parseInt(matEl.value, 10),
          sa = parseInt(saEl.value, 10);
      out.style.display = "none";
      if (isNaN(age)) { show(""); return; }
      if (age < minAge || age > maxAge) { show("Age at entry must be between " + minAge + " and " + maxAge + "."); return; }
      if (isNaN(mat)) { show(""); return; }
      if (isNaN(sa)) { show(""); return; }
      if (sa <= 0 || sa % 1000 !== 0 || sa > 100000000) {
        show("Enter a sum assured in multiples of \u20B91,000 (up to \u20B910 crore)."); return;
      }
      var br = parseFloat(bonusEl.value);
      if (!isNaN(br) && (br < 0 || br > 1000)) { show("Enter a bonus rate between 0 and 1000."); return; }
      var r = calc(rates, age, mat, sa, isNaN(br) ? undefined : br);
      if (!r) { show("This combination is not available in the rate table."); return; }
      show("");
      document.getElementById("pli-rate").textContent = "\u20B9" + r.rate.toFixed(2) + " per \u20B91,000";
      document.getElementById("pli-term").textContent = r.term + " years";
      document.getElementById("pli-monthly").textContent = inr(r.monthly);
      document.getElementById("pli-yearly").textContent = inr(r.yearly);
      document.getElementById("pli-total").textContent = inr(r.total);
      var hasBonus = r.bonus !== undefined;
      document.getElementById("pli-bonus-row").style.display = hasBonus ? "" : "none";
      document.getElementById("pli-maturity-row").style.display = hasBonus ? "" : "none";
      if (hasBonus) {
        document.getElementById("pli-bonus-amt").textContent = inr(r.bonus);
        document.getElementById("pli-maturity").textContent = inr(r.maturityAmount);
      }
      out.style.display = "block";
    }

    ageEl.addEventListener("input", function () { fillMaturity(); update(); });
    matEl.addEventListener("change", update);
    saEl.addEventListener("input", update);
    bonusEl.addEventListener("input", update);
    fillMaturity();
  });
})(typeof window !== "undefined" ? window : globalThis);
