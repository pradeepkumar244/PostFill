/* RPLI premium calculator. Runs entirely in the browser; nothing is sent to the server. */
(function (root) {
  "use strict";

  var MODES = [
    { key: "monthly", label: "Monthly", perYear: 12 },
    { key: "quarterly", label: "Quarterly", perYear: 4 },
    { key: "annual", label: "Yearly", perYear: 1 }
  ];

  function options(rates, age) {
    var row = rates.monthly[String(age)];
    if (!row) return [];
    return Object.keys(row).map(Number).sort(function (a, b) { return a - b; })
      .map(function (m) { return { maturity: m, term: m - age }; });
  }

  // Instalment = rate per Rs 1,000 x (sum assured / 1,000). Integer paise maths avoids float drift.
  function calc(rates, age, maturity, sumAssured, bonusRate) {
    if (!Number.isInteger(sumAssured) || sumAssured <= 0 || sumAssured % 1000 !== 0) return null;
    var term = maturity - age, modes = [];
    for (var i = 0; i < MODES.length; i++) {
      var row = rates[MODES[i].key][String(age)];
      if (!row || row[String(maturity)] === undefined) return null;
      var rate = row[String(maturity)];
      var paise = Math.round(rate * 100) * (sumAssured / 1000);
      modes.push({
        key: MODES[i].key, label: MODES[i].label, rate: rate,
        instalment: paise / 100,
        perYear: (paise * MODES[i].perYear) / 100,
        total: (paise * MODES[i].perYear * term) / 100
      });
    }
    var res = { term: term, modes: modes };
    // bonus = (sum assured / 1000) x bonus rate x term; maturity amount = sum assured + bonus
    if (typeof bonusRate === "number" && bonusRate >= 0) {
      res.bonus = Math.round((sumAssured / 1000) * bonusRate * term * 100) / 100;
      res.maturityAmount = sumAssured + res.bonus;
    }
    return res;
  }

  var api = { options: options, calc: calc, MODES: MODES };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
  root.RPLI = api;
  if (typeof document === "undefined") return;

  document.addEventListener("DOMContentLoaded", function () {
    var dataEl = document.getElementById("rpli-data");
    if (!dataEl) return;
    var rates = JSON.parse(dataEl.textContent);
    var ageEl = document.getElementById("rpli-age"), matEl = document.getElementById("rpli-mat"),
        saEl = document.getElementById("rpli-sa"), bonusEl = document.getElementById("rpli-bonus"),
        err = document.getElementById("rpli-err"), out = document.getElementById("rpli-out"),
        body = document.getElementById("rpli-modes");
    var minAge = Number(ageEl.min), maxAge = Number(ageEl.max),
        minSa = Number(saEl.min), maxSa = Number(saEl.max);

    function inr(n) {
      return "\u20B9" + n.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }
    function show(msg) { err.textContent = msg; err.style.display = msg ? "block" : "none"; }
    function set(id, text) { document.getElementById(id).textContent = text; }

    function fillMaturity() {
      var age = parseInt(ageEl.value, 10), prev = matEl.value;
      matEl.innerHTML = "";
      var opts = (age >= minAge && age <= maxAge) ? options(rates, age) : [];
      if (!opts.length) { matEl.innerHTML = '<option value="">Enter a valid age first</option>'; return; }
      opts.forEach(function (o) {
        var el = document.createElement("option");
        el.value = o.maturity;
        el.textContent = "Age " + o.maturity + " (" + o.term + " years)";
        matEl.appendChild(el);
      });
      if (prev && matEl.querySelector('option[value="' + prev + '"]')) matEl.value = prev;
    }

    function update() {
      var age = parseInt(ageEl.value, 10), mat = parseInt(matEl.value, 10), sa = parseInt(saEl.value, 10);
      out.style.display = "none";
      if (isNaN(age)) { show(""); return; }
      if (age < minAge || age > maxAge) { show("Age at entry must be between " + minAge + " and " + maxAge + "."); return; }
      if (isNaN(mat) || isNaN(sa)) { show(""); return; }
      if (sa % 1000 !== 0 || sa < minSa || sa > maxSa) {
        show("Enter a sum assured in multiples of \u20B91,000, from \u20B9" + minSa.toLocaleString("en-IN") +
             " to \u20B9" + maxSa.toLocaleString("en-IN") + "."); return;
      }
      var br = parseFloat(bonusEl.value);
      if (!isNaN(br) && (br < 0 || br > 1000)) { show("Enter a bonus rate between 0 and 1000."); return; }
      var r = calc(rates, age, mat, sa, isNaN(br) ? undefined : br);
      if (!r) { show("This combination is not available in the rate table."); return; }
      show("");
      set("rpli-term", r.term + " years");
      body.textContent = "";
      r.modes.forEach(function (m) {
        var tr = document.createElement("tr");
        [m.label, "\u20B9" + m.rate.toFixed(2), inr(m.instalment), inr(m.perYear), inr(m.total)].forEach(function (t, i) {
          var c = document.createElement(i === 0 ? "th" : "td"); if (i === 0) c.scope = "row";
          c.textContent = t; tr.appendChild(c);
        });
        body.appendChild(tr);
      });
      var has = r.bonus !== undefined;
      document.getElementById("rpli-bonus-row").style.display = has ? "" : "none";
      document.getElementById("rpli-maturity-row").style.display = has ? "" : "none";
      if (has) { set("rpli-bonus-amt", inr(r.bonus)); set("rpli-maturity", inr(r.maturityAmount)); }
      out.style.display = "block";
    }

    ageEl.addEventListener("input", function () { fillMaturity(); update(); });
    matEl.addEventListener("change", update);
    saEl.addEventListener("input", update);
    bonusEl.addEventListener("input", update);
    fillMaturity();
  });
})(typeof window !== "undefined" ? window : globalThis);
