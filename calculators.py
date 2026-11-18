"""Post office scheme calculators: page content and default rates.

Default rates are those notified for 1 October - 31 December 2026. The government
reviews them every quarter: update the numbers below (and RATES_PERIOD) when they change.
Users can also edit the rate on each page.
"""

RATES_PERIOD = "1 October – 31 December 2026"

_MODE = [["year", "Once a year (before 5 April)"], ["month", "Every month (before the 5th)"]]

CALCS = [
 {
  "slug": "rd-calculator", "key": "rd", "name": "RD Calculator",
  "h1": "Post Office RD Calculator",
  "summary": "Maturity value of a monthly Recurring Deposit.",
  "desc": "Free post office Recurring Deposit (RD) calculator. Enter a monthly deposit to see total deposit, interest and maturity value with quarterly compounding.",
  "intro": "See what a monthly Recurring Deposit grows into. Enter the amount you can save each month and the calculator shows your total deposit, interest and maturity value.",
  "inputs": [
    {"id": "amount", "label": "Monthly deposit (₹)", "type": "number", "value": 5000, "min": 100, "step": 10},
    {"id": "years", "label": "Tenure", "type": "select", "value": 5, "options": [[5, "5 years"], [10, "10 years (after 5-year extension)"]]},
  ],
  "rate": 6.7,
  "body": """
<h2>How the post office RD works</h2>
<p>You deposit a fixed amount every month for five years. Interest is compounded every quarter and paid with your money at maturity. The rate in force on the day you open the account applies for the full five years, so a later rate cut does not affect an existing RD.</p>
<h2>How this calculator estimates it</h2>
<p>Each monthly instalment is grown at the quarterly-compounded rate for the months it stays in the account, and the amounts are added together. Real passbook figures can differ by a few rupees because of rounding and the exact deposit dates.</p>
<h2>Good to know</h2>
<ul>
<li>The minimum deposit is ₹100 a month, in multiples of ₹10, with no upper limit.</li>
<li>Deposits made after the 15th of a month count from the next month. Missing instalments leads to a small default fee.</li>
<li>An RD can be extended for another five years. For the extension the calculator assumes the same rate, which may not match the rate at that time.</li>
<li>Interest is taxable. Check the current rules for TDS and your tax slab.</li>
</ul>
"""
 },
 {
  "slug": "td-calculator", "key": "td", "name": "TD (Fixed Deposit) Calculator",
  "h1": "Post Office TD (Time Deposit) Calculator",
  "summary": "Interest and maturity value for 1, 2, 3 and 5-year deposits.",
  "desc": "Free post office Time Deposit (TD) calculator for 1, 2, 3 and 5 year terms. See yearly interest, total interest and maturity value.",
  "intro": "Choose a deposit amount and a term of 1, 2, 3 or 5 years to see how much interest a post office Time Deposit earns. The rate fills in automatically for the term you pick.",
  "inputs": [
    {"id": "amount", "label": "Deposit amount (₹)", "type": "number", "value": 100000, "min": 1000, "step": 100},
    {"id": "years", "label": "Term", "type": "select", "value": 5, "options": [[1, "1 year"], [2, "2 years"], [3, "3 years"], [5, "5 years"]]},
  ],
  "rate": 7.5, "rate_by": {"input": "years", "map": {"1": 6.9, "2": 7.0, "3": 7.1, "5": 7.5}},
  "body": """
<h2>How the post office Time Deposit works</h2>
<p>A Time Deposit (TD) is the post office version of a fixed deposit. You deposit a lump sum for 1, 2, 3 or 5 years at a rate fixed on the day you open it. Interest is calculated every quarter and is paid out once a year.</p>
<h2>Two ways to read the result</h2>
<p>If you take the interest every year, you receive the yearly amount shown and your principal comes back at the end. If you instead leave the interest in the account, it earns more interest, and the maturity value shows what that would grow to at the same rate. Choose what suits your goal: regular income, or maximum growth.</p>
<h2>Good to know</h2>
<ul>
<li>The minimum deposit is ₹1,000, in multiples of ₹100, with no maximum.</li>
<li>Only the 5-year TD qualifies for a Section 80C deduction, and only under the old tax regime. Interest is taxable for all terms.</li>
<li>Closing early is possible after six months but at a lower rate, so check the rules before you commit.</li>
</ul>
"""
 },
 {
  "slug": "mis-calculator", "key": "mis", "name": "MIS Calculator",
  "h1": "Post Office MIS (Monthly Income Scheme) Calculator",
  "summary": "Monthly interest income from the Monthly Income Scheme.",
  "desc": "Free post office Monthly Income Scheme (MIS) calculator. See your monthly interest, yearly income and total interest over 5 years for single and joint accounts.",
  "intro": "Enter your MIS deposit to see the interest you will receive every month, every year and over the five-year term.",
  "inputs": [
    {"id": "amount", "label": "Deposit amount (₹)", "type": "number", "value": 900000, "min": 1000, "step": 1000},
    {"id": "type", "label": "Account type", "type": "select", "value": "single", "options": [["single", "Single (up to ₹9 lakh)"], ["joint", "Joint (up to ₹15 lakh)"]]},
  ],
  "rate": 7.4,
  "body": """
<h2>How the Monthly Income Scheme works</h2>
<p>You deposit a lump sum for five years and receive interest every month. The interest is not added to your balance. It is paid out, so it works as a steady monthly income, and your full deposit comes back at maturity. Many people link the account to a savings account so the interest is credited automatically.</p>
<h2>How this calculator estimates it</h2>
<p>Monthly interest is the deposit multiplied by the yearly rate and divided by twelve, rounded to the nearest rupee. Because the interest is paid out and not reinvested, there is no compounding. The rate in force on the day you open the account applies for the whole term.</p>
<h2>Good to know</h2>
<ul>
<li>The minimum deposit is ₹1,000, in multiples of ₹1,000.</li>
<li>The maximum is ₹9 lakh in a single account and ₹15 lakh in a joint account, counted across all your MIS accounts.</li>
<li>Early closure is generally allowed only after one year, with a small deduction from the deposit, so confirm the rules with your branch.</li>
<li>Interest is taxable at your slab rate, and MIS does not qualify for a Section 80C deduction.</li>
<li>At maturity you can withdraw the deposit or reinvest it in a new account at the then-current rate.</li>
</ul>
"""
 },
 {
  "slug": "scss-calculator", "key": "scss", "name": "SCSS Calculator",
  "h1": "Senior Citizens' Savings Scheme (SCSS) Calculator",
  "summary": "Quarterly interest and 5-year income from SCSS.",
  "desc": "Free SCSS calculator: see quarterly interest, yearly interest and total interest on a Senior Citizens' Savings Scheme deposit of up to ₹30 lakh.",
  "intro": "Enter your SCSS deposit to see the interest you will receive every quarter, every year and over the full five years.",
  "inputs": [
    {"id": "amount", "label": "Deposit amount (₹)", "type": "number", "value": 1000000, "min": 1000, "step": 1000},
  ],
  "rate": 8.2,
  "body": """
<h2>How SCSS works</h2>
<p>The Senior Citizens' Savings Scheme is designed to give retired people a regular income. Interest is not added to your balance. It is paid out every quarter, so the income stays steady, and your full deposit comes back at maturity after five years.</p>
<h2>Who can open it</h2>
<p>Residents aged 60 or above can open an account. People who retired under a superannuation or voluntary scheme can open one from age 55, and defence service retirees from age 50, subject to the scheme conditions. A spouse can hold a joint account.</p>
<h2>Good to know</h2>
<ul>
<li>The minimum deposit is ₹1,000 in multiples of ₹1,000, and the maximum across all SCSS accounts is ₹30 lakh.</li>
<li>Interest is credited on the first working day of April, July, October and January.</li>
<li>The account can be extended once for three more years.</li>
<li>Interest is taxable and TDS may apply above a threshold. The deposit can qualify for 80C under the old tax regime.</li>
</ul>
"""
 },
 {
  "slug": "ppf-calculator", "key": "ppf", "name": "PPF Calculator",
  "h1": "PPF Calculator (Public Provident Fund)",
  "summary": "Year-by-year PPF balance and maturity value.",
  "desc": "Free PPF calculator with year-wise table. See your Public Provident Fund maturity amount, total investment and interest for 15 to 35 years.",
  "intro": "Enter how much you invest in PPF each year and for how long. You will see the maturity value and a year-by-year table of deposits, interest and balance.",
  "inputs": [
    {"id": "amount", "label": "Yearly investment (₹)", "type": "number", "value": 150000, "min": 500, "step": 500},
    {"id": "mode", "label": "How you deposit", "type": "select", "value": "year", "options": _MODE},
    {"id": "years", "label": "Duration", "type": "select", "value": 15, "options": [[15, "15 years"], [20, "20 years (1 extension)"], [25, "25 years (2 extensions)"], [30, "30 years (3 extensions)"], [35, "35 years (4 extensions)"]]},
  ],
  "rate": 7.1,
  "body": """
<h2>How PPF works</h2>
<p>The Public Provident Fund has a 15-year term that can be extended in blocks of five years. You can deposit between ₹500 and ₹1.5 lakh in a financial year. Interest is worked out on the lowest balance between the 5th and the end of each month and is added to your account once a year, on 31 March.</p>
<h2>Why the deposit date matters</h2>
<p>Money deposited before the 5th of a month earns interest for that month. That is why depositing the full yearly amount early in April gives a slightly higher maturity value than spreading it through the year. Use the option above to compare the two.</p>
<h2>A floating rate</h2>
<p>Unlike a fixed-term scheme, the PPF rate is reviewed every quarter and applies to your whole balance. This calculator assumes today's rate for every year, so your actual result will move up or down if the rate changes.</p>
<h2>Good to know</h2>
<ul>
<li>The contribution (under the old regime), the interest and the maturity amount have traditionally been tax-free. Check the latest tax rules.</li>
<li>Partial withdrawals are allowed from the seventh financial year, and a loan can be taken in the early years.</li>
<li>Deposits above ₹1.5 lakh in a year earn no interest.</li>
</ul>
"""
 },
 {
  "slug": "ssa-calculator", "key": "ssa", "name": "Sukanya Samriddhi (SSA) Calculator",
  "h1": "Sukanya Samriddhi Yojana (SSY) Calculator",
  "summary": "Maturity value of a Sukanya Samriddhi Account at 21 years.",
  "desc": "Free Sukanya Samriddhi Yojana (SSY) calculator. Enter the yearly deposit and the girl's age to see the maturity value at 21 years, with a year-wise table.",
  "intro": "Plan your daughter's future fund. Enter the yearly deposit and your daughter's age when you open the account to see the maturity value.",
  "inputs": [
    {"id": "amount", "label": "Yearly deposit (₹)", "type": "number", "value": 150000, "min": 250, "step": 250},
    {"id": "mode", "label": "How you deposit", "type": "select", "value": "year", "options": _MODE},
    {"id": "age", "label": "Girl's age when opening (0–9)", "type": "number", "value": 1, "min": 0, "max": 9, "step": 1},
  ],
  "rate": 8.2,
  "body": """
<h2>How the Sukanya Samriddhi Account works</h2>
<p>You open the account in the name of a girl child below 10 years of age. Deposits are made for 15 years from the date of opening, and the account matures 21 years after opening. For the last six years you do not deposit anything, but the balance keeps earning interest.</p>
<h2>How this calculator estimates it</h2>
<p>It works like PPF: interest is calculated on the monthly lowest balance and credited once a year. The result uses today's rate for all 21 years. The SSA rate is reviewed every quarter, so the actual maturity value will differ if the rate changes.</p>
<h2>Good to know</h2>
<ul>
<li>Yearly deposits can be anywhere from ₹250 to ₹1.5 lakh.</li>
<li>Up to 50% of the balance can generally be withdrawn for higher education once the girl turns 18 or passes the 10th standard.</li>
<li>A family can usually open accounts for two girls, with an exception for twins or triplets.</li>
<li>A missed yearly minimum makes the account default; it can be revived with a small penalty.</li>
</ul>
"""
 },
 {
  "slug": "kvp-calculator", "key": "kvp", "name": "KVP Calculator",
  "h1": "Kisan Vikas Patra (KVP) Calculator",
  "summary": "Maturity amount and doubling period of Kisan Vikas Patra.",
  "desc": "Free Kisan Vikas Patra (KVP) calculator: see how long your money takes to double and the maturity amount at the current rate.",
  "intro": "Enter your KVP investment to see the maturity amount and how many months it takes to double.",
  "inputs": [
    {"id": "amount", "label": "Investment amount (₹)", "type": "number", "value": 100000, "min": 1000, "step": 100},
  ],
  "rate": 7.5,
  "body": """
<h2>How KVP works</h2>
<p>Kisan Vikas Patra is a lump-sum certificate that doubles your money after a fixed number of months. The government sets that period from the interest rate. At 7.5% a year, compounded annually, the money doubles in 115 months, which is 9 years and 7 months.</p>
<h2>How the doubling period is found</h2>
<p>The calculator divides the time needed to double at the rate you enter, using annual compounding, and rounds it to whole months. At the current rate this gives the notified 115 months. The government publishes the exact period for each rate, so treat the figure for other rates as an estimate.</p>
<h2>Good to know</h2>
<ul>
<li>The minimum investment is ₹1,000, in multiples of ₹100, with no maximum.</li>
<li>The rate on the day you buy applies until maturity, so a later rate cut does not shorten or lengthen your period.</li>
<li>Interest is taxable. KVP does not qualify for a Section 80C deduction.</li>
<li>A certificate can be encashed early only after a lock-in and in specific cases, so confirm the rules with your branch.</li>
</ul>
"""
 },
 {
  "slug": "nsc-calculator", "key": "nsc", "name": "NSC Calculator",
  "h1": "National Savings Certificate (NSC) Calculator",
  "summary": "5-year NSC maturity value with year-wise growth.",
  "desc": "Free NSC calculator: see the maturity value, total interest and year-wise growth of a 5-year National Savings Certificate.",
  "intro": "Enter your NSC investment to see what it grows to after five years, with the value at the end of each year.",
  "inputs": [
    {"id": "amount", "label": "Investment amount (₹)", "type": "number", "value": 100000, "min": 1000, "step": 100},
  ],
  "rate": 7.7,
  "body": """
<h2>How NSC works</h2>
<p>The National Savings Certificate has a five-year term. Interest is compounded every year but paid only at maturity, together with your principal. The rate on the day you buy it stays fixed for all five years.</p>
<h2>Tax treatment</h2>
<p>The amount invested qualifies for a Section 80C deduction under the old tax regime. The interest is taxable, but the interest accrued in the first four years is treated as reinvested and so also qualifies for deduction in those years. The interest for the fifth year is taxable without that benefit. Check the latest rules before you invest.</p>
<h2>Good to know</h2>
<ul>
<li>The minimum investment is ₹1,000, in multiples of ₹100, with no maximum.</li>
<li>Certificates can be bought by adults, joint holders, and on behalf of minors.</li>
<li>They can be pledged as security for a loan.</li>
<li>Early encashment is allowed only in limited situations, such as the death of the holder.</li>
</ul>
"""
 },
]

BY_SLUG = {c["slug"]: c for c in CALCS}
