from flask import Flask, render_template_string, request, send_file
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
import os

app = Flask(__name__)

# HTML form template
HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>PDF Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
        h1 { text-align: center; }
        form { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        label { font-weight: bold; margin-top: 10px; display: block; }
        input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 100%; }
        .row { display: flex; gap: 10px; margin-bottom: 10px; }
        .col { flex: 1; }
        button { padding: 10px 20px; background: #4CAF50; border: none; color: white; font-size: 16px; cursor: pointer; border-radius: 4px; }
        button:hover { background: #45a049; }
        .charges-table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        .charges-table th, .charges-table td { border: 1px solid #ccc; padding: 8px; }
        .charges-table th { background: #f0f0f0; }
    </style>
    <script>
        function updateTotal() {
            let fields = [
                "cf_charges", "godown_rent", "courier_charges", "electric_bill",
                "internet_charges", "local_freight", "labour_charges", "hamali_charges"
            ];
            let total = 0;
            fields.forEach(id => {
                let val = parseFloat(document.querySelector(`[name="${id}"]`).value) || 0;
                total += val;
            });
            document.querySelector('[name="total"]').value = total.toFixed(2);
        }
    </script>
</head>
<body>
    <h1>Fill PDF Template</h1>
    <form method="post" action="/generate">
        <div class="row">
            <div class="col">
                <label>Name:</label>
                <input name="name" required>
            </div>
            <div class="col">
                <label>Date:</label>
                <input name="date" required>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <label>From:</label>
                <input name="from_addr" required>
            </div>
            <div class="col">
                <label>To:</label>
                <input name="to_addr" required>
            </div>
        </div>

        <table class="charges-table">
            <tr>
                <th>Charge Type</th>
                <th>Amount</th>
                <th>Remarks</th>
            </tr>
            {% for charge, remarks in charge_fields %}
            <tr>
                <td>{{ charge.replace('_', ' ').title() }}</td>
                <td><input name="{{ charge }}" oninput="updateTotal()"></td>
                <td><input name="{{ remarks }}"></td>
            </tr>
            {% endfor %}
        </table>

        <label>Total:</label>
        <input name="total" readonly required>

        <button type="submit">Generate PDF</button>
    </form>
</body>
</html>
"""

# Function to create overlay
def create_overlay(data):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(612, 792))  # Letter size
    
    # Name with larger font
    can.setFont("Helvetica-Bold", 12)
    can.drawString(80, 620, str(data.get("name", "")))

    # Rest of the details with normal font
    can.setFont("Helvetica", 10)
    can.drawString(464, 680, str(data.get("date", "")))
    can.drawString(330, 530, str(data.get("from_addr", "")))
    can.drawString(410, 530, str(data.get("to_addr", "")))

    # Charges + Remarks
    y_start = 465
    step = 17
    charge_fields = [
        ("cf_charges", "cf_remarks"),
        ("godown_rent", "godown_remarks"),
        ("courier_charges", "courier_remarks"),
        ("electric_bill", "electric_remarks"),
        ("internet_charges", "internet_remarks"),
        ("local_freight", "local_remarks"),
        ("labour_charges", "labour_remarks"),
        ("hamali_charges", "hamali_remarks"),
    ]

    for i, (charge, remark) in enumerate(charge_fields):
        y = y_start - (i * step)
        can.drawString(320, y, str(data.get(charge, "")))
        can.drawString(413, y, str(data.get(remark, "")))

    # Total
    can.setFont("Helvetica-Bold", 12)
    can.drawString(320, 328, str(data.get("total", "")))

    can.save()
    packet.seek(0)
    return packet

# Merge overlay with template
def fill_pdf(template_path, data):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file '{template_path}' not found")

    template_pdf = PdfReader(open(template_path, "rb"))
    overlay_pdf = PdfReader(create_overlay(data))

    writer = PdfWriter()
    page = template_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

@app.route("/", methods=["GET"])
def form():
    charge_fields = [
        ("cf_charges", "cf_remarks"),
        ("godown_rent", "godown_remarks"),
        ("courier_charges", "courier_remarks"),
        ("electric_bill", "electric_remarks"),
        ("internet_charges", "internet_remarks"),
        ("local_freight", "local_remarks"),
        ("labour_charges", "labour_remarks"),
        ("hamali_charges", "hamali_remarks"),
    ]
    return render_template_string(HTML_FORM, charge_fields=charge_fields)

@app.route("/generate", methods=["POST"])
def generate():
    data = {key: request.form[key] for key in request.form}

    # List of charge field names
    charge_fields = [
        "cf_charges",
        "godown_rent",
        "courier_charges",
        "electric_bill",
        "internet_charges",
        "local_freight",
        "labour_charges",
        "hamali_charges"
    ]

    # Calculate total
    total = 0
    for field in charge_fields:
        try:
            total += float(data.get(field, 0) or 0)
        except ValueError:
            pass  # ignore non-numeric inputs

    # Store total in data
    data["total"] = str(round(total, 2))

    pdf_bytes = fill_pdf("template.pdf", data)
    return send_file(pdf_bytes, as_attachment=True, download_name="filled.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)