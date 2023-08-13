from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.units import inch
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

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

    # Calculate row heights to cover the whole canvas with 23px margin
    row_height = (available_height - 23 * 2) / len(data)

    # Create a table with the data and adjusted cell dimensions
    table_data = []
    for i in range(len(data)):
        # Create a radar plot
        angles = np.linspace(0, 2 * np.pi, 5, endpoint=False)
        values = [i * 10 + 10, i * 10 + 20, i * 10 + 15, i * 10 + 5, i * 10 + 10]  # Example data
        radar_fig = plt.figure(figsize=(cell_width / inch, row_height / inch), dpi=80)
        radar_ax = radar_fig.add_subplot(111, polar=True)
        radar_ax.plot(angles, values)
        radar_ax.fill(angles, values, alpha=0.25)
        plt.xticks(angles, ['A', 'B', 'C', 'D', 'E'])
        radar_canvas = FigureCanvas(radar_fig)
        radar_buffer = BytesIO()
        radar_canvas.print_png(radar_buffer)
        plt.close(radar_fig)
        radar_image = Image(radar_buffer, width=cell_width, height=row_height)  # Use row_height here
        
        # Create a pie chart
        pie_fig = plt.figure(figsize=(cell_width / inch, row_height / inch), dpi=80)
        pie_ax = pie_fig.add_subplot(111)
        labels = ['A', 'B', 'C', 'D', 'E']
        sizes = [20, 30, 15, 10, 25]  # Example data
        pie_ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
        pie_ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        pie_canvas = FigureCanvas(pie_fig)
        pie_buffer = BytesIO()
        pie_canvas.print_png(pie_buffer)
        plt.close(pie_fig)
        pie_image = Image(pie_buffer, width=cell_width, height=row_height)  # Use row_height here
        
        # Append the radar plot and pie chart to the table data
        table_data.append([radar_image, pie_image])

    table = Table(table_data, colWidths=[cell_width, cell_width], rowHeights=[row_height] * len(data))

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
