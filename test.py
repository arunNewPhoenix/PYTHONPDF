from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Create a PDF document
doc = SimpleDocTemplate("table_with_images.pdf", pagesize=letter)

# Sample data for the table
data = [
    [Image("image1.png", width=50, height=50), Paragraph("Heading 1", getSampleStyleSheet()["Heading1"])],
    [Image("image2.jpg", width=50, height=50), ""],
]

# Define table style with black border
table_style = TableStyle([
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add black border
])
# Create the table with the data and style
table = Table(data)
table.setStyle(table_style)

# Build the story and generate the PDF
doc.build([table])
