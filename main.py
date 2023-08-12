from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def generate_pdf():
    # Create a PDF document with a margin of 23 pixels from all sides
    doc = SimpleDocTemplate("table_example.pdf", pagesize=letter, leftMargin=23, rightMargin=23, topMargin=23, bottomMargin=23)

    # Define data for the table (2 columns and 5 rows)
    data = [
        ["Cell 1"],
        ["Cell 2"],
        ["Cell 3"],
        ["Cell 4"],
    ]

    # Calculate available width and height after considering margins
    available_width = doc.pagesize[0] - doc.leftMargin - doc.rightMargin
    available_height = doc.pagesize[1] - doc.topMargin - doc.bottomMargin

    # Calculate cell width and height
    cell_width = (available_width - 23) / 2  # Divide by 2 for 2 columns
    cell_height = (available_height - 3 * inch) / len(data)

    # Create a table with the data and adjusted cell dimensions
    table_data = []
    for i in range(len(data)):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [i * 10 + 10, i * 10 + 20, i * 10 + 15, i * 10 + 5])
        canvas = FigureCanvas(fig)
        buffer = BytesIO()
        canvas.print_png(buffer)
        plt.close(fig)
        image = Image(buffer, width=cell_width, height=cell_height)
        empty_cell = Spacer(width=cell_width, height=cell_height)  # Empty cell
        table_data.append([image, empty_cell])

    table = Table(table_data, colWidths=[cell_width, cell_width], rowHeights=[cell_height] * len(data))

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