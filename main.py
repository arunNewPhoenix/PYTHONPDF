from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

app = Flask(__name__)

@app.route('/')
def generate_pdf():
    # Create a PDF document with a margin of 23 pixels from all sides
    doc = SimpleDocTemplate("table_example.pdf", pagesize=letter, leftMargin=23, rightMargin=23, topMargin=23, bottomMargin=23)

    # Define data for the table (2 columns and 4 rows)
    data = [
        ["Row 1, Col 1", "Row 1, Col 2"],
        ["Row 2, Col 1", "Row 2, Col 2"],
        ["Row 3, Col 1", "Row 3, Col 2"],
        ["Row 4, Col 1", "Row 4, Col 2"],
    ]

    # Calculate available width and height after considering margins
    available_width = doc.pagesize[0] - doc.leftMargin - doc.rightMargin
    available_height = doc.pagesize[1] - doc.topMargin - doc.bottomMargin

    # Calculate cell width
    cell_width = available_width / len(data[0])

    # Calculate cell height to fit 3 rows within the available height
    cell_height = (available_height - 3 * inch) / 3

    # Create a table with the data and adjusted cell dimensions
    table = Table(data, colWidths=[cell_width] * len(data[0]), rowHeights=[cell_height] * len(data))

    # Add style to the table (black border for all cells)
    style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Black border for all cells
    ])

    table.setStyle(style)

    # Build the PDF document
    elements = [table]
    doc.build(elements)

    return send_file("table_example.pdf")

if __name__ == '__main__':
    app.run(debug=True)

