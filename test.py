import pandas as pd
import plotly.express as px
from fpdf import FPDF
from PIL import Image

# Create a simple DataFrame for demonstration
data = {'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 15, 7, 12]}

df = pd.DataFrame(data)

# Create a bar chart using Plotly
fig = px.bar(df, x='Category', y='Value', title='Simple Bar Chart')

# Save the Plotly chart as an image
chart_filename = 'bar_chart.png'
fig.write_image(chart_filename, engine='kaleido')

# Create a PDF and add the chart image to it using FPDF
pdf_filename = 'bar_chart.pdf'

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Simple Bar Chart', align='C', ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = PDF()
pdf.add_page()

# Open the chart image using PIL (Pillow)
image = Image.open(chart_filename)

# Define the image width and height in the PDF
pdf_width, pdf_height = 210, 297  # A4 paper size in millimeters
aspect_ratio = float(image.width) / float(image.height)
img_width = pdf_width
img_height = pdf_width / aspect_ratio

# Add the chart image to the PDF
pdf.image(chart_filename, x=5, y=20, w=img_width, h=img_height)

# Output the PDF file
pdf.output(pdf_filename)

print(f"PDF file '{pdf_filename}' has been created.")
