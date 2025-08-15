from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io

# Step 1: Get template size
def get_pdf_size(template_path):
    reader = PdfReader(template_path)
    page = reader.pages[0]
    width = float(page.mediabox[2])
    height = float(page.mediabox[3])
    return width, height

# Step 2: Create a coordinate grid for reference
def create_coordinate_grid(width, height):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont("Helvetica", 6)

    # Vertical lines with X values
    for x in range(0, int(width), 20):
        can.drawString(x + 2, 5, str(x))
        can.line(x, 0, x, height)

    # Horizontal lines with Y values
    for y in range(0, int(height), 20):
        can.drawString(2, y + 2, str(y))
        can.line(0, y, width, y)

    can.save()
    packet.seek(0)
    return packet

# Step 3: Create overlay with actual text
def create_overlay(width, height, name, date, amount, coords):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    can.setFont("Helvetica-Bold", 12)

    # coords is a dict with positions for each field
    can.drawString(coords["name"][0], coords["name"][1], name)
    can.drawString(coords["date"][0], coords["date"][1], date)
    can.drawString(coords["amount"][0], coords["amount"][1], f"${amount}")

    can.save()
    packet.seek(0)
    return packet

# Step 4: Merge overlay with template
def merge_pdfs(template_path, overlay_packet, output_path):
    template_pdf = PdfReader(template_path)
    overlay_pdf = PdfReader(overlay_packet)

    writer = PdfWriter()
    page = template_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

# --- Main Usage ---
template_path = "template.pdf"

# Get exact size of template
width, height = get_pdf_size(template_path)

# 1️⃣ Create coordinate grid to find positions
grid_overlay = create_coordinate_grid(width, height)
merge_pdfs(template_path, grid_overlay, "coordinate_helper.pdf")
print("✅ Coordinate helper PDF generated: 'coordinate_helper.pdf'")
print("   Open it, find the coordinates for name/date/amount, then update them below.")

# 2️⃣ Once you have coordinates, fill PDF
coords = {
    "name": (100, 700),   # Change after checking coordinate_helper.pdf
    "date": (100, 680),
    "amount": (400, 650)
}

# Uncomment to actually fill PDF once you know positions
# overlay = create_overlay(width, height, "John Doe", "2025-08-14", "1234.56", coords)
# merge_pdfs(template_path, overlay, "filled.pdf")
# print("✅ Filled PDF generated: 'filled.pdf'")
