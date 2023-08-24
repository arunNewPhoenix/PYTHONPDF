from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def generate_pdf():
    # Define the PDF file name
    pdf_file_name = "rounded_rectangle_with_text.pdf"

    # Create a canvas
    c = canvas.Canvas(pdf_file_name, pagesize=letter)

    # Set the line width and line color for the rectangle
    line_width = 2  # Adjust the line width as needed
    line_color = (0, 0, 0)  # Adjust the line color as needed (black in RGB)

    # Draw a rounded rectangle
    x, y, width, height = 100, 500, 400, 200  # Adjust the position, width, and height as needed
    radius = 20  # Adjust the corner radius as needed

    c.setLineWidth(line_width)
    c.setStrokeColorRGB(*line_color)
    c.roundRect(x, y, width, height, radius)

    # Add a heading inside the rectangle
    heading = "Rounded Rectangle with Text"
    c.setFont("Helvetica-Bold", 14)  # Set the font and size for the heading
    c.drawString(x + 20, y + height - 20, heading)

    # Add three points on different lines
    points = [
        "Point 1: This is the first point.",
        "Point 2: This is the second point.",
        "Point 3: This is the third point.",
    ]
    c.setFont("Helvetica", 12)  # Set the font and size for the points
    for i, point in enumerate(points):
        line_y = y + height - 50 - (i * 20)
        c.drawString(x + 20, line_y, point)

    # Add a string 34 points below the rectangle
    text_below_rect = "This is 34 points below the rectangle."
    c.setFont("Helvetica", 12)  # Set the font and size for the text
    text_y = y - 104  # Calculate the y position 34 points below the rectangle
    c.drawString(x + 10, text_y, text_below_rect)

    # Save the PDF file
    c.save()

    return send_file(pdf_file_name)

if __name__ == '__main__':
    app.run(debug=True)



