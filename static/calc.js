/* Post office scheme calculators. Runs in the browser; nothing is sent to the server. */
(function (root) {
  "use strict";

  var S = {};
  var DEPOSIT_LIMIT = 150000;

  function rupee(n) { return n.toLocaleString("en-IN", { maximumFractionDigits: 0 }); }
  function inr(n) { return "\u20B9" + rupee(Math.round(n)); }
  function ym(m) {
    var y = Math.floor(m / 12), r = m % 12, p = [];
    if (y) p.push(y + (y === 1 ? " year" : " years"));
    if (r) p.push(r + (r === 1 ? " month" : " months"));
    return p.join(" ") + " (" + m + " months)";
  }

  // Recurring Deposit: each monthly instalment grows at quarterly-compounded interest.
  S.rd = function (v, r) {
    var P = v.amount, n = v.years * 12, i = r / 400, m = 0;
    if (!(P >= 100) || P % 10 !== 0) return { error: "Monthly deposit must be at least \u20B9100, in multiples of \u20B910." };
    for (var k = 1; k <= n; k++) m += P * Math.pow(1 + i, k / 3);
    return { rows: [["Total deposited", inr(P * n)], ["Interest earned", inr(m - P * n)], ["Maturity value", inr(m), true]] };
  };

  // Time Deposit: quarterly compounding, interest paid yearly.
  S.td = function (v, r) {
    var P = v.amount, t = v.years, i = r / 400;
    if (!(P >= 1000) || P % 100 !== 0) return { error: "Deposit must be at least \u20B91,000, in multiples of \u20B9100." };
    var yearly = P * (Math.pow(1 + i, 4) - 1), mat = P * Math.pow(1 + i, 4 * t);
    return { rows: [
      ["Amount deposited", inr(P)],
      ["Interest paid each year", inr(yearly)],
      ["Total interest if paid out yearly", inr(yearly * t)],
      ["Maturity value if interest is left to grow", inr(mat), true],
      ["Effective yearly return", ((Math.pow(1 + i, 4) - 1) * 100).toFixed(2) + "%"]
    ] };
  };

  // SCSS: simple interest paid every quarter, principal returned after 5 years.
  S.scss = function (v, r) {
    var P = v.amount;
    if (!(P >= 1000) || P % 1000 !== 0) return { error: "Deposit must be at least \u20B91,000, in multiples of \u20B91,000." };
    if (P > 3000000) return { error: "The maximum SCSS deposit is \u20B930 lakh." };
    var q = Math.round(P * r / 400);
    return { rows: [
      ["Interest every quarter", inr(q), true],
      ["Interest every year", inr(q * 4)],
      ["Total interest in 5 years", inr(q * 20)],
      ["Deposit returned at maturity", inr(P)],
      ["Total received over 5 years", inr(P + q * 20)]
    ] };
  };

  // MIS: simple interest paid every month, principal returned after 5 years.
  S.mis = function (v, r) {
    var P = v.amount, max = v.type === "joint" ? 1500000 : 900000;
    if (!(P >= 1000) || P % 1000 !== 0) return { error: "Deposit must be at least \u20B91,000, in multiples of \u20B91,000." };
    if (P > max) return { error: "The maximum is " + (v.type === "joint" ? "\u20B915 lakh for a joint account." : "\u20B99 lakh for a single account.") };
    var m = Math.round(P * r / 1200);
    return { rows: [
      ["Interest every month", inr(m), true],
      ["Interest every year", inr(m * 12)],
      ["Total interest in 5 years", inr(m * 60)],
      ["Deposit returned at maturity", inr(P)],
      ["Total received over 5 years", inr(P + m * 60)]
    ] };
  };

  // PPF and SSA: interest on the lowest monthly balance, credited once a year.
  function provident(Y, mode, rate, depositYears, totalYears) {
    var bal = 0, dep = 0, rows = [], r = rate / 100;
    for (var y = 1; y <= totalYears; y++) {
      var d = y <= depositYears ? Y : 0, interest = 0;
      if (mode === "month") {
        for (var m = 1; m <= 12; m++) interest += (bal + (d / 12) * m) * r / 12;
      } else {
        interest = (bal + d) * r;
      }
      bal += d + interest; dep += d;
      rows.push([String(y), inr(d), inr(interest), inr(bal)]);
    }
    return { bal: bal, dep: dep, rows: rows };
  }

  S.ppf = function (v, r) {
    if (!(v.amount >= 500) || v.amount > DEPOSIT_LIMIT) return { error: "Yearly investment must be between \u20B9500 and \u20B91,50,000." };
    var p = provident(v.amount, v.mode, r, v.years, v.years);
    return {
      rows: [["Total invested", inr(p.dep)], ["Interest earned", inr(p.bal - p.dep)], ["Maturity value", inr(p.bal), true]],
      table: { head: ["Year", "Deposit", "Interest", "Balance"], rows: p.rows }
    };
  };

  S.ssa = function (v, r) {
    if (!(v.amount >= 250) || v.amount > DEPOSIT_LIMIT) return { error: "Yearly deposit must be between \u20B9250 and \u20B91,50,000." };
    if (!Number.isInteger(v.age) || v.age < 0 || v.age > 9) return { error: "The girl must be below 10 years old when the account is opened." };
    var p = provident(v.amount, v.mode, r, 15, 21);
    return {
      rows: [["Total deposited (15 years)", inr(p.dep)], ["Interest earned", inr(p.bal - p.dep)],
             ["Maturity value after 21 years", inr(p.bal), true], ["Girl's age at maturity", String(v.age + 21)]],
      table: { head: ["Year", "Deposit", "Interest", "Balance"], rows: p.rows }
    };
  };

  // KVP: money doubles; the period follows from the annual-compounded rate.
  S.kvp = function (v, r) {
    var P = v.amount;
    if (!(P >= 1000) || P % 100 !== 0) return { error: "Investment must be at least \u20B91,000, in multiples of \u20B9100." };
    var months = Math.round(Math.log(2) / Math.log(1 + r / 100) * 12);
    return { rows: [["Maturity amount", inr(P * 2), true], ["Interest earned", inr(P)], ["Time to double", ym(months)]] };
  };

  // NSC: annual compounding, paid at maturity after 5 years.
  S.nsc = function (v, r) {
    var P = v.amount;
    if (!(P >= 1000) || P % 100 !== 0) return { error: "Investment must be at least \u20B91,000, in multiples of \u20B9100." };
    var rows = [], prev = P;
    for (var y = 1; y <= 5; y++) {
      var val = P * Math.pow(1 + r / 100, y);
      rows.push([String(y), inr(val - prev), inr(val)]); prev = val;
    }
    return {
      rows: [["Amount invested", inr(P)], ["Interest earned", inr(prev - P)], ["Maturity value after 5 years", inr(prev), true]],
      table: { head: ["Year", "Interest for the year", "Value at year end"], rows: rows }
    };
  };

  function run(key, values, rate) {
    if (!(rate > 0 && rate <= 20)) return { error: "Enter an interest rate between 0 and 20." };
    for (var k in values) if (typeof values[k] === "number" && isNaN(values[k])) return null;
    return S[key](values, rate);
  }

  var api = { run: run, schemes: S };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; }
  root.CALC = api;
  if (typeof document === "undefined") return;

  document.addEventListener("DOMContentLoaded", function () {
    var specEl = document.getElementById("calc-spec");
    if (!specEl) return;
    var spec = JSON.parse(specEl.textContent);
    var form = document.getElementById("calc-form"), out = document.getElementById("calc-out"),
        err = document.getElementById("calc-err"), rateEl = document.getElementById("in-rate");

    function values() {
      var v = {};
      Array.prototype.forEach.call(form.querySelectorAll("[data-in]"), function (el) {
        var id = el.getAttribute("data-in");
        if (el.tagName === "SELECT") v[id] = isNaN(Number(el.value)) ? el.value : Number(el.value);
        else v[id] = el.value === "" ? NaN : parseFloat(el.value);
      });
      return v;
    }
    function el(tag, text, cls) {
      var e = document.createElement(tag);
      if (text !== undefined) e.textContent = text;
      if (cls) e.className = cls;
      return e;
    }
    function render() {
      out.textContent = ""; err.style.display = "none";
      var res = run(spec.key, values(), parseFloat(rateEl.value));
      if (!res) { out.style.display = "none"; return; }
      if (res.error) { err.textContent = res.error; err.style.display = "block"; out.style.display = "none"; return; }
      out.appendChild(el("h2", "Your result")).style.marginTop = "0";
      res.rows.forEach(function (r) {
        var line = el("div", "", "line" + (r[2] ? " main" : ""));
        line.appendChild(el("span", r[0])); line.appendChild(el("strong", r[1]));
        out.appendChild(line);
      });
      if (res.table) {
        var wrap = el("div", "", "tablewrap"), t = el("table", "", "rates"), tr = el("tr");
        res.table.head.forEach(function (h) { tr.appendChild(el("th", h)); });
        var thead = el("thead"); thead.appendChild(tr); t.appendChild(thead);
        var tb = el("tbody");
        res.table.rows.forEach(function (row) {
          var r = el("tr"); row.forEach(function (c) { r.appendChild(el("td", c)); }); tb.appendChild(r);
        });
        t.appendChild(tb); wrap.appendChild(t);
        out.appendChild(el("h3", "Year-wise breakdown")); out.appendChild(wrap);
      }
      out.style.display = "block";
    }

    if (spec.rate_by) {
      var src = form.querySelector('[data-in="' + spec.rate_by.input + '"]');
      src.addEventListener("change", function () {
        var r = spec.rate_by.map[src.value]; if (r !== undefined) rateEl.value = r;
        render();
      });
    }
    form.addEventListener("input", render);
    form.addEventListener("change", render);
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    render();
  });
})(typeof window !== "undefined" ? window : globalThis);
