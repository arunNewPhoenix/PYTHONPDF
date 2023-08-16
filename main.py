from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO

app = Flask(__name__)

# Function to generate a radar plot
def generate_radar_chart(data, labels, width, height):
    fig = plt.figure(figsize=(width / inch, height / inch), dpi=80)
    ax = fig.add_subplot(111, polar=True)
    angles = np.linspace(0, 2 * np.pi, len(data), endpoint=False)
    ax.plot(angles, data)
    ax.fill(angles, data, alpha=0.25)
    plt.xticks(angles, labels)
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)

# Function to generate a pie chart
def generate_pie_chart(sizes, labels, width, height):
    fig = plt.figure(figsize=(width / inch, height / inch), dpi=80)
    ax = fig.add_subplot(111)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)

# Function to generate an area chart
def generate_area_chart(data, labels, width, height):
    fig = plt.figure(figsize=(width / inch, height / inch), dpi=80)
    ax = fig.add_subplot(111)
    ax.stackplot(range(len(data[0])), data, labels=labels)
    ax.legend(loc='upper left')
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)

# Function to generate a bar chart
def generate_bar_chart(data, labels, width, height):
    fig = plt.figure(figsize=(width / inch, height / inch), dpi=80)
    ax = fig.add_subplot(111)
    ax.bar(labels, data)
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)

# Function to generate a doughnut chart
def generate_doughnut_chart(data, labels, width, height):
    fig, ax = plt.subplots(figsize=(width / inch, height / inch), dpi=80)
    ax.pie(data, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, wedgeprops={'edgecolor': 'white'})
    center_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(center_circle)
    ax.axis('equal')
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)

# Function to generate a line chart
def generate_line_chart(data, labels, width, height):
    fig = plt.figure(figsize=(width / inch, height / inch), dpi=80)
    ax = fig.add_subplot(111)
    for line_data, label in zip(data, labels):
        ax.plot(range(len(line_data)), line_data, label=label)
    ax.legend(loc='upper left')
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)


# Function to generate a polar chart
def generate_polar_chart(data, labels, width, height):
    fig = plt.figure(figsize=(width / inch, height / inch), dpi=80)
    ax = fig.add_subplot(111, projection='polar')
    angles = np.linspace(0, 2 * np.pi, len(data), endpoint=False)
    for line_data, label in zip(data, labels):
        ax.plot(angles, line_data, label=label)
    ax.legend(loc='upper right')
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    canvas = FigureCanvas(fig)
    buffer = BytesIO()
    canvas.print_png(buffer)
    plt.close(fig)
    return Image(buffer, width=width, height=height)




@app.route('/')
def generate_pdf():
    doc = SimpleDocTemplate("table_example.pdf", pagesize=letter, leftMargin=23, rightMargin=23, topMargin=23, bottomMargin=23)

    radar_data = [i * 10 + 10 for i in range(5)]
    radar_labels = ['A', 'B', 'C', 'D', 'E']
    pie_sizes = [20, 30, 15, 10, 25]
    pie_labels = ['A', 'B', 'C', 'D', 'E']

    # Sample data for doughnut chart
    doughnut_data = [25, 35, 20, 10, 10]
    doughnut_labels = ['A', 'B', 'C', 'D', 'E']


    # Sample data for radar chart
    radar_data = [30, 40, 20, 50, 60]
    radar_labels = ['A', 'B', 'C', 'D', 'E']


    # Sample data for area chart
    area_data = [
    [10, 20, 30, 40, 50],
    [20, 30, 40, 30, 20]
    ]
    area_labels = ['Series 1', 'Series 2']

    # Sample data for bar chart
    bar_data = [25, 40, 10, 30, 50]
    bar_labels = ['A', 'B', 'C', 'D', 'E']


    available_width = doc.pagesize[0] - doc.leftMargin - doc.rightMargin
    available_height = doc.pagesize[1] - doc.topMargin - doc.bottomMargin

    cell_width = (available_width - 23) / 2
    cell_height = (available_height - 4 * inch) / 2

    table_data = [
        [
            generate_radar_chart(radar_data, radar_labels, cell_width, cell_height),
            generate_pie_chart(pie_sizes, pie_labels, cell_width, cell_height)
        ],
        [
            "Your Heading Text Here",
            Image("image1.png", width=cell_width, height=cell_height)
        ],
        [
            "Heading 2",
            Image("image2.jpg", width=cell_width, height=cell_height)
        ],
      [
            "Your Heading Text Here",
            generate_area_chart(area_data, area_labels, cell_width, cell_height)
        ],
        [
            "Heading 2",
            generate_bar_chart(bar_data, bar_labels, cell_width, cell_height)
        ],
        [
            "DoughNut Chart",
            generate_doughnut_chart(doughnut_data,doughnut_labels,cell_width,cell_height)
        ]
     
        
    ]

    # Create the Table object with the chart data
    table = Table(table_data, colWidths=[cell_width, cell_width], rowHeights=[cell_height, cell_height,cell_height,cell_height,cell_height,cell_height]) #add cell_height here to add more rows
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Build the PDF document
    elements = [table]
    doc.build(elements)

    return send_file("table_example.pdf")

if __name__ == '__main__':
    app.run(debug=True)



