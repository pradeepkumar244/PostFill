
from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
import sqlite3
from flask import jsonify

app = Flask(__name__)
def save_customer(data):
    conn = sqlite3.connect("customers.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        cif TEXT PRIMARY KEY,
        applicant_name TEXT,
        father_name TEXT,
        dob TEXT,
        gender TEXT,
        aadhaar TEXT,
        pan TEXT,
        mobile TEXT,
        email TEXT,
        present_address TEXT,
        permanent_address TEXT
    )
    """)

    cur.execute("""
    INSERT OR REPLACE INTO customers
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("cif", ""),
        data.get("applicant_name", ""),
        data.get("father_name", ""),
        data.get("dob", ""),
        data.get("gender", ""),
        data.get("aadhaar", ""),
        data.get("pan", ""),
        data.get("mobile", ""),
        data.get("email", ""),
        data.get("present_address", ""),
        data.get("permanent_address", "")
    ))

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/customer/<cif>")
def customer(cif):

    conn = sqlite3.connect("customers.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM customers WHERE cif=?", (cif,))
    row = cur.fetchone()

    conn.close()

    if row:
        return jsonify({
            "applicant_name": row[1],
            "father_name": row[2],
            "dob": row[3],
            "gender": row[4],
            "aadhaar": row[5],
            "pan": row[6],
            "mobile": row[7],
            "email": row[8],
            "present_address": row[9],
            "permanent_address": row[10]
        })

    return jsonify({})


@app.route("/generate", methods=["POST"])
def generate():

    data = request.form.to_dict()

    template_pdf = "pdf_templates/SB-AOF.pdf"

    reader = PdfReader(template_pdf)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):

        packet = BytesIO()

        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        c = canvas.Canvas(packet, pagesize=(width, height))

        # PAGE 1
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

            c.drawString(194, 262, data.get("present_address", ""))
            c.drawString(194, 227, data.get("permanent_address", ""))

            c.drawString(194, 217, data.get("mobile", ""))
            c.drawString(194, 205, data.get("email", ""))

            c.setFont("Helvetica-Bold", 9)
            c.drawString(136, 422, data.get("deposit", ""))
            c.drawString(204, 422, data.get("deposit_words", ""))

        

        # PAGE 2
        if page_num == 1:

            c.setFont("Helvetica", 8)

            c.drawString(64, 349, data.get("nominee_name", ""))
            c.drawString(71, 325, data.get("nominee_relation", ""))
            c.drawString(424, 352, data.get("nominee_share", ""))

        c.save()

        packet.seek(0)

        overlay = PdfReader(packet)

        page.merge_page(overlay.pages[0])

        writer.add_page(page)

    output_pdf = "generated_forms/final_form.pdf"

    with open(output_pdf, "wb") as output:
        writer.write(output)

    save_customer(data)
    return send_file(
        output_pdf,
        as_attachment=True,
        download_name="PostOffice_Form.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)

