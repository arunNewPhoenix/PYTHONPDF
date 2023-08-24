from flask import Flask, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def generate_pdf():
    # Define the PDF file name
    pdf_file_name = "rounded_rectangle_with_text.pdf"

    # Create a canvas
    c = canvas.Canvas(pdf_file_name, pagesize=letter)

    # Load the image (replace 'image_path.png' with the path to your image file)
    image_path = 'psylief.png'  # Replace with your image path
    img = ImageReader(image_path)

    # Calculate image width and height (you can adjust this as needed)
    image_width = 200
    image_height = 70

    # Calculate the position for the image (centered at the top of the page)
    image_x = letter[0] - 500
    image_y = letter[1] -  140

    # Draw the image at the top of the page
    c.drawImage(img, x=image_x, y=image_y, width=image_width, height=image_height, mask='auto')

    # Set the line width and line color for the rectangle
    line_width = 2  # Adjust the line width as needed
    line_color = (248/255, 218/255, 105/255)  # RGB color: #f8da69

    # Draw a rounded rectangle below the image
    x, y, width, height = 100, image_y - 280, 400, 200  # Adjust the position, width, and height as needed
    radius = 20  # Adjust the corner radius as needed

    c.setLineWidth(line_width)
    c.setStrokeColorRGB(*line_color)
    c.roundRect(x, y, width, height, radius)

    # Add a heading inside the rectangle
    heading = "Rounded Rectangle with Text"
    c.setFont("Helvetica-Bold", 14)  # Set the font and size for the heading
    c.drawString(x + 20, y + height - 20, heading)

    # Set the font and size for the points
    font_size = 12
    c.setFont("Helvetica-Bold", font_size)

    # Calculate the initial y position for the points
    line_y = y + height - 50

    # Add three points on different lines inside the rectangle
    points = [
        "Point 1: This is the first point.",
        "Point 2: This is the second point.",
        "Point 3: This is the third point.",
    ]

    # Set a fixed vertical spacing between points
    vertical_spacing = 20

    # Draw the points with consistent font size and spacing
    for point in points:
        c.drawString(x + 20, line_y, point)
        line_y -= vertical_spacing  # Adjust the y position for the next point

    # Add another string just below the third point with a different font size
    current_time = datetime.now().strftime("%B %d, %Y %I:%M %p")  # Format the current time
    additional_text = f"Test Time: {current_time}"
    c.setFont("Helvetica-Bold", 10)  # Set a different font size
    additional_text_y = y + height - (len(points) + 1) * vertical_spacing - 80  # Adjust the position
    c.drawString(x + 20, additional_text_y, additional_text)

    # Add a string below the rectangle
    text_below_rect = "Career Counselling changes"
    c.setFont("Helvetica-Bold", 12)  # Set the font and size for the text
    text_y = y - 184  # Adjust the y position for the text
    c.drawString(x + 20, text_y, text_below_rect)

    # Add another string just below the text_below_rect
    additional_text_below = "Test Report"
    additional_text_below_y = text_y - vertical_spacing  # Adjust the position
    c.drawString(x + 20, additional_text_below_y, additional_text_below)

    # Save the PDF file
    c.save()

    return send_file(pdf_file_name)

if __name__ == '__main__':
    app.run(debug=True)


