from flask import Flask, send_file
from reportlab.lib.pagesizes import letter,A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer, Indenter,ListFlowable,ListItem
from reportlab.lib import colors
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Paragraph
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
    doc = SimpleDocTemplate("table_example.pdf", pagesize=A4, leftMargin=23, rightMargin=23, topMargin=23 )

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

    cell_width = (available_width- 23) / 2
    cell_height = (doc.pagesize[1] - 2 * inch) / 2
    

    sub_cell_width = cell_width / 2  # Adjust sub-cell width
    sub_cell_height = cell_height / 2  # Adjust sub-cell height


    # Define styles
    styles = getSampleStyleSheet()
    bullet_style = styles['Normal']
    bullet_style.leading = 12  # Adjust spacing between lines

    bottom_margin = 20
    top_margin = 10  
    cell_style = TableStyle([
    ('TOPPADDING', (0, 0), (-1, -1), top_margin),    
    ('BOTTOMPADDING', (0, 0), (-1, -1), bottom_margin),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('VALIGN', (0, 0), (-1, -1), 'TOP')  # Align all cells in the cell_style at the top
])
     # Create bullet points for each sub-cell
    sub_cell_bullet_points = [
        "Sub-heading 1:\nExtroverts gain energy from people, situations and things around them which can also be called as “the outer world”. They are sociable and like being with people. They like to go and explore the outer world and try new things.",
        "Sub-heading 2:\nExtroverts gain energy from people, situations and things around them which can also be called as “the outer world”. They are sociable and like being with people. They like to go and explore the outer world and try new things.",
        "Sub-heading 3:\nExtroverts gain energy from people, situations and things around them which can also be called as “the outer world”. They are sociable and like being with people. They like to go and explore the outer world and try new things.",
        "Sub-heading 4:\nExtroverts gain energy from people, situations and things around them which can also be called as “the outer world”. They are sociable and like being with people. They like to go and explore the outer world and try new things."
    ]

    defination = "ESTJs rely on objective information and logic to make decisions rather than personal feelings. They are skilled at making objective, impersonal, and impartial decisions. Rather than focusing on their own subjective feelings when they are making judgments, they consider facts and logic in order to make rational choices. People with ESTJ personality types tend to be very practical. They enjoy learning about things that they can see an immediate, real-world use for, but tend to lose interest in things that are abstract or theoretical. ESTJs enjoy concrete facts as opposed to abstract information."
    sub_heading_height = 30  # Set the desired spacing for the sub-heading row
    sub_cell_height = 150  # Set the desired height for the sub-cell rows

# Create the sub-table data with adjusted sub-heading height
    sub_table_data = [
    [
        Paragraph("<b>Sub-Table Heading</b>", styles['Normal']),
        None
    ],
    [
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_bullet_points[0], bullet_style),
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_bullet_points[1], bullet_style)
    ],
    [
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_bullet_points[2], bullet_style, 'top'),
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_bullet_points[3], bullet_style, 'top')
    ]
]

# Set the row heights for the sub-table
    sub_table_row_heights = [sub_heading_height] + [sub_cell_height] * (len(sub_table_data) - 1)

# Create the sub-table with adjusted row heights
    sub_table = Table(sub_table_data, colWidths=[sub_cell_width, sub_cell_width], rowHeights=sub_table_row_heights)
    sub_table.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ('VALIGN', (0, 0), (-1, 0), 'TOP'),  # Align heading cell at the top
    ('VALIGN', (0, 1), (-1, -1), 'TOP')  # Align all other cells in the sub-table at the top
]))
    extra_space = 5
    
    # Create bullet points for sub-table_2
    sub_table_2_bullet_points = [
    "First bullet point in sub-table_2.",
    "Second bullet point in sub-table_2.",
    "Third bullet point in sub-table_2.",
    "Fourth bullet point in sub-table_2."
]

    sub_2_heading_height   = 25
    sub_2_cell_height = 76
# Calculate the height of sub-table_2 rows
    sub_table_2_row_height = [sub_2_heading_height] + [sub_2_cell_height] * (len(sub_table_2_bullet_points))

# Define a style for the bold heading
    bold_style = ParagraphStyle(name='BoldStyle')
    bold_style.fontName = 'Helvetica-Bold'

# Create the data for sub-table_2
    sub_table_2_data = [
    [Paragraph("<b>Sub-Table_2 Heading</b>", bold_style)],
]

# Add bullet points with adjusted row height
    for bullet_point in sub_table_2_bullet_points:
        sub_table_2_data.append([Paragraph("<bullet>&bull;</bullet> " + bullet_point, bullet_style)])
# Double the width of each cell in sub_table_2
    sub_cell_width_2 = sub_cell_width * 2  # Double the width of each cell

# Create sub-table_2 with double width and adjusted row heights
    sub_table_2 = Table(sub_table_2_data, colWidths=[sub_cell_width_2], rowHeights=sub_table_2_row_height)
    sub_table_2.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ('VALIGN', (0, 0), (-1, 0), 'TOP'),  # Align heading cell at the top
    ('VALIGN', (0, 1), (-1, -1), 'TOP')  # Align all other cells in sub-table_2 at the top
]))

    
    # Create bullet points for each sub-cell
    sub_cell_3_bullet_points = [
        "Sub-heading 1:\n outer world and try new things.",
        "Sub-heading 2:\n They like to go and explore the outer world and try new things.",
        "Sub-heading 3:\n go and explore the outer world and try new things.",
        "Sub-heading 4:\n They like to go and explore the outer world and try new things.",
        "Sub-heading 5:\n They like to go and explore the outer world and try new things.",
        "Sub-heading 6:\n They like to go and explore the outer world and try new things.",
        "Sub-heading 7:\n They like to go and explore the outer world and try new things.",
        "Sub-heading 8:\n They like to go and explore the outer world and try new things.",
    ]

    
    sub_heading_3_height = 30  # Set the desired spacing for the sub-heading row
    sub_cell_3_height = 70  # Set the desired height for the sub-cell rows

# Create the sub-table data with adjusted sub-heading height
    sub_table_3_data = [
    [
        Paragraph("<b>Sub-Table Heading</b>", styles['Normal']),
        None
    ],
    [
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[0], bullet_style),
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[1], bullet_style)
    ],
    [
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[2], bullet_style, 'top'),
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[3], bullet_style, 'top')
    ]
     ,
     [
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[4], bullet_style, 'top'),
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[5], bullet_style, 'top')
    ]
     ,
     [
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[6], bullet_style, 'top'),
        Paragraph("<bullet>&bull;</bullet> " + sub_cell_3_bullet_points[7], bullet_style, 'top')
    ]
]

# Set the row heights for the sub-table
    sub_table_3_row_heights = [sub_heading_3_height] + [sub_cell_3_height] * (len(sub_table_3_data) - 1)

# Create the sub-table with adjusted row heights
    sub_table_3 = Table(sub_table_3_data, colWidths=[sub_cell_width, sub_cell_width], rowHeights=sub_table_3_row_heights)
    sub_table_3.setStyle(TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ('VALIGN', (0, 0), (-1, 0), 'TOP'),  # Align heading cell at the top
    ('VALIGN', (0, 1), (-1, -1), 'TOP')  # Align all other cells in the sub-table at the top
]))

    table_data = [
    [
        generate_radar_chart(radar_data, radar_labels, cell_width, cell_height),
        generate_pie_chart(pie_sizes, pie_labels, cell_width, cell_height)
    ],
    [
        sub_table,  # Use the nested table here
        generate_area_chart(area_data, area_labels, cell_width, cell_height)
    ],
    [
         Paragraph("<font size='12'><b>Sub-Cell Heading</b></font><br/>" +
              "<br/>" * extra_space +  # Add extra space here
              "<bullet>&bull;</bullet> " + defination, styles['Normal']),
        Image("image2.png", width=cell_width, height=cell_height)
    ],
    [
        sub_table_2 ,
        generate_bar_chart(bar_data, bar_labels, cell_width, cell_height)
    ],
    [
        sub_table_3,
        generate_doughnut_chart(doughnut_data, doughnut_labels, cell_width, cell_height)
    ]
]



    # Create the Table object with the chart data
    table = Table(table_data, colWidths=[cell_width, cell_width], rowHeights=[cell_height] * 5)  # Adjust rowHeights as needed
    style = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(cell_style)
    # Build the PDF document
    elements = [table]
    doc.build(elements)

    return send_file("table_example.pdf")

if __name__ == '__main__':
    app.run(debug=True)



