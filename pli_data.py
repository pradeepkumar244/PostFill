"""PLI premium rate table.

Monthly premium rate per Rs 1,000 sum assured, by age at entry (rows) and age at
maturity (columns). Blank cells mean that combination is not offered.
To change rates, edit RAW below (same layout as the Google Sheet) and redeploy.
"""

MATURITY_AGES = [35, 40, 45, 50, 55, 58, 60]

# Each row: entry age followed by the rates. Rates are right-aligned, i.e. a row with
# fewer values than columns starts at a later maturity age (shorter terms are not offered).
RAW = """
19 5.15 3.75 2.95 2.35 1.95 1.75 1.75
20 5.35 3.95 3.15 2.55 1.95 1.95 1.75
21 5.75 4.15 3.15 2.55 2.15 1.95 1.75
22 6.35 4.35 3.35 2.75 2.15 1.95 1.95
23 6.95 4.75 3.55 2.75 2.35 2.15 1.95
24 7.55 5.15 3.75 2.95 2.35 2.15 1.95
25 8.35 5.35 3.95 3.15 2.55 2.15 2.15
26 9.35 5.75 4.15 3.15 2.55 2.35 2.15
27 10.55 6.35 4.35 3.35 2.75 2.35 2.35
28 12.15 6.95 4.75 3.55 2.75 2.55 2.35
29 14.35 7.55 5.15 3.75 2.95 2.55 2.55
30 17.15 8.35 5.55 3.95 3.15 2.75 2.55
31 9.35 5.95 4.15 3.35 2.95 2.75
32 10.55 6.35 4.55 3.35 2.95 2.75
33 12.15 6.95 4.75 3.55 3.15 2.95
34 14.35 7.55 5.15 3.75 3.35 2.95
35 17.15 8.35 5.55 3.95 3.55 3.15
36 9.35 5.95 4.35 3.75 3.35
37 10.55 6.35 4.55 3.95 3.55
38 12.15 6.95 4.95 4.15 3.75
39 14.35 7.75 5.15 4.35 3.95
40 17.35 8.55 5.55 4.55 4.15
41 9.55 5.95 4.95 4.35
42 10.75 6.55 5.35 4.75
43 12.35 7.15 5.75 4.95
44 14.35 7.75 6.15 5.35
45 17.35 8.55 6.55 5.75
46 9.55 7.15 6.15
47 10.95 7.95 6.75
48 12.55 8.75 7.35
49 14.55 9.75 7.95
50 17.55 10.95 8.75
51 12.95 10.35
52 14.95 11.75
53 17.75 13.15
54 15.15
55 17.95
"""


def _parse():
    rates = {}
    for line in RAW.strip().splitlines():
        parts = line.split()
        age, vals = int(parts[0]), [float(v) for v in parts[1:]]
        cols = MATURITY_AGES[len(MATURITY_AGES) - len(vals):]
        rates[age] = dict(zip(cols, vals))
    return rates


RATES = _parse()
MIN_AGE, MAX_AGE = min(RATES), max(RATES)


# Bonus per Rs 1,000 sum assured for every completed year of the policy (from your sheet: *52).
# The department declares the actual rate each year, so update this when it changes.
BONUS_RATE_PER_1000 = 52
