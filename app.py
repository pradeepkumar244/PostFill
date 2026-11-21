import os
from datetime import date
from io import BytesIO

from flask import Flask, Response, abort, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from calculators import BY_SLUG, CALCS, RATES_PERIOD
from content import GUIDES
from pli_data import BONUS_RATE_PER_1000, MATURITY_AGES, MAX_AGE, MIN_AGE, RATES
import rpli_data

# ---------------------------------------------------------------- settings --
# Set these as environment variables on your host (or edit the defaults).
SITE_NAME = "PostFill"
SITE_URL = os.environ.get("SITE_URL", "https://www.example.com").rstrip("/")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "postfill24x7@gmail.com")
# AdSense publisher id, e.g. "ca-pub-1234567890123456". Leave empty until you have one.
ADSENSE_CLIENT = os.environ.get("ADSENSE_CLIENT", "")
# Ad-unit slot ids (created in AdSense after approval). Empty = no ad rendered.
AD_SLOT_ARTICLE = os.environ.get("AD_SLOT_ARTICLE", "")
AD_SLOT_HOME = os.environ.get("AD_SLOT_HOME", "")

TEMPLATE_PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf_templates", "SB-AOF.pdf")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # the form is tiny; reject large posts


@app.context_processor
def inject_globals():
    return dict(site_name=SITE_NAME, site_url=SITE_URL, contact_email=CONTACT_EMAIL,
                adsense_client=ADSENSE_CLIENT, ad_slot_article=AD_SLOT_ARTICLE,
                ad_slot_home=AD_SLOT_HOME, year=date.today().year,
                canonical=SITE_URL + request.path)


# --------------------------------------------------------- security headers --
_GOOGLE_ADS = ("https://pagead2.googlesyndication.com https://*.googlesyndication.com "
               "https://*.google.com https://*.doubleclick.net https://*.googleadservices.com "
               "https://adservice.google.com https://partner.googleadservices.com "
               "https://googleads.g.doubleclick.net https://tpc.googlesyndication.com")

CSP = "; ".join([
    "default-src 'self'",
    f"script-src 'self' 'unsafe-inline' {_GOOGLE_ADS}",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: https:",
    f"connect-src 'self' {_GOOGLE_ADS}",
    f"frame-src {_GOOGLE_ADS}",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'self'",
])


@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = CSP
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    if request.is_secure or request.headers.get("X-Forwarded-Proto") == "https":
        resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    if request.path == "/generate":
        # the response contains personal data: never cache it anywhere
        resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
        resp.headers["Pragma"] = "no-cache"
    return resp


# ------------------------------------------------------------------ pages ---
@app.route("/")
def home():
    return render_template("home.html", guides=GUIDES)


@app.route("/form")
def form():
    return render_template("tool.html")


@app.route("/calculators")
def calculators():
    return render_template("calculators.html", calcs=CALCS, rates_period=RATES_PERIOD)


@app.route("/calculators/<slug>")
def calculator(slug):
    c = BY_SLUG.get(slug)
    if not c:
        abort(404)
    spec = {"key": c["key"], "rate_by": c.get("rate_by")}
    return render_template("calc.html", c=c, spec=spec, rates_period=RATES_PERIOD,
                           others=[x for x in CALCS if x["slug"] != slug])


@app.route("/pli-calculator")
def pli_calculator():
    return render_template("pli.html", rates=RATES, maturity_ages=MATURITY_AGES,
                           min_age=MIN_AGE, max_age=MAX_AGE,
                           bonus_rate=BONUS_RATE_PER_1000)

@app.route("/rpli-calculator")
def rpli_calculator():
    return render_template("rpli.html", rates=rpli_data.RATES, maturity_ages=rpli_data.MATURITY_AGES,
                           min_age=rpli_data.MIN_AGE, max_age=rpli_data.MAX_AGE,
                           min_sa=rpli_data.MIN_SUM_ASSURED, max_sa=rpli_data.MAX_SUM_ASSURED,
                           bonus_rate=rpli_data.BONUS_RATE_PER_1000)
@app.route("/guides")
def guides():
    return render_template("guides.html", guides=GUIDES)


@app.route("/guides/<slug>")
def guide(slug):
    g = next((x for x in GUIDES if x["slug"] == slug), None)
    if not g:
        abort(404)
    others = [x for x in GUIDES if x["slug"] != slug][:4]
    return render_template("guide.html", g=g, others=others)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacy-policy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


# ------------------------------------------------- crawler / AdSense files --
@app.route("/robots.txt")
def robots():
    body = f"User-agent: *\nAllow: /\nDisallow: /generate\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@app.route("/ads.txt")
def ads_txt():
    if not ADSENSE_CLIENT:
        abort(404)
    pub = ADSENSE_CLIENT.replace("ca-", "", 1)  # ca-pub-123 -> pub-123
    return Response(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    paths = ["/", "/form", "/calculators", "/pli-calculator", "/rpli-calculator", "/guides", "/about", "/contact", "/privacy-policy",
             "/terms", "/disclaimer"] + [f"/calculators/{c['slug']}" for c in CALCS] \
        + [f"/guides/{g['slug']}" for g in GUIDES]
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc></url>" for p in paths)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    return Response(xml, mimetype="application/xml")


# ------------------------------------------------------------- PDF filling --
def draw_wrapped_text(c, text, x, y, max_width=120, font="Helvetica", font_size=8, leading=10):
    c.setFont(font, font_size)
    for line in simpleSplit(str(text or ""), font, font_size, max_width):
        c.drawString(x, y, line)
        y -= leading


@app.route("/generate", methods=["POST"])
def generate():
    data = {k: v[:300] for k, v in request.form.to_dict().items()}

    reader = PdfReader(TEMPLATE_PDF)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        packet = BytesIO()
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        c = canvas.Canvas(packet, pagesize=(width, height))

        # ---- PAGE 1 (coordinates unchanged from the original app) ----
        if page_num == 0:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(48, 611, data.get("applicant_name", ""))

            c.setFont("Helvetica-Bold", 16)
            c.drawString(23, 594, data.get("scheme", ""))

            c.setFont("Helvetica-Bold", 18)
            cif = str(data.get("cif", ""))
            x = 403
            y = 744
            gap = 19
            for digit in cif:
                c.drawString(x, y, digit)
                x += gap

            c.setFont("Helvetica", 8)
            c.drawString(194, 380, data.get("applicant_name", ""))
            c.drawString(194, 365, data.get("father_name", ""))
            c.drawString(194, 356, data.get("gender", ""))
            c.drawString(194, 334, data.get("dob", ""))
            c.drawString(194, 322, data.get("aadhaar", ""))
            c.drawString(194, 308, data.get("pan", ""))

            draw_wrapped_text(c, data.get("present_address", ""), 194, 282)
            draw_wrapped_text(c, data.get("permanent_address", ""), 194, 247)

            c.drawString(194, 217, data.get("mobile", ""))
            c.drawString(194, 205, data.get("email", ""))

            c.setFont("Helvetica-Bold", 9)
            c.drawString(136, 422, data.get("deposit", ""))
            c.drawString(204, 422, data.get("deposit_words", ""))

        # ---- PAGE 2 ----
        if page_num == 1:
            c.setFont("Helvetica", 8)
            c.drawString(64, 360, data.get("nominee_name", ""))
            c.drawString(71, 349, f'({data.get("nominee_relation", "")})')
            c.drawString(424, 360, f'{data.get("nominee_share", "")}%')

        c.save()
        packet.seek(0)
        page.merge_page(PdfReader(packet).pages[0])
        writer.add_page(page)

    # Built entirely in memory and streamed back. Nothing about the customer is
    # written to disk or to a database, so there is nothing to leak or mix up.
    out = BytesIO()
    writer.write(out)
    out.seek(0)
    return send_file(out, mimetype="application/pdf", as_attachment=True,
                     download_name="PostOffice_Form.pdf")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
