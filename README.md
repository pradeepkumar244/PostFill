# PostFill (AdSense-ready)

No database, no customer storage, no CIF lookup. PDFs are generated in memory and returned to the
user; nothing is written to disk.

## Environment variables
- SITE_URL        e.g. https://www.yourdomain.com (sitemap + canonical links)
- CONTACT_EMAIL   a real email shown on the Contact and Privacy pages
- ADSENSE_CLIENT  ca-pub-XXXXXXXXXXXXXXXX (adds the AdSense script and serves /ads.txt)
- AD_SLOT_ARTICLE, AD_SLOT_HOME  ad-unit ids from AdSense (no ads are drawn while empty)

## Run
pip install -r requirements.txt
python app.py              # local
gunicorn app:app           # production (Procfile included)

## Adding guides
Append a dict to GUIDES in content.py (slug, title, summary, body). It appears on the site and
in sitemap.xml automatically.

## PLI calculator
Rates live in pli_data.py (same layout as the sheet). Logic is in static/pli.js and runs in the browser.
Test: node -e "const P=require('./static/pli.js');console.log(P.calc({'19':{'35':5.15}},19,35,100000))"

## Scheme calculators
Default rates and page text are in calculators.py (update RATES_PERIOD and the rates every quarter).
Formulas are in static/calc.js and run in the browser.
