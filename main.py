import base64
import qrcode
from PIL import Image
import io
import sys
import os
from htmlmin import minify  # Import the minify function from the htmlmin module


def minify_html(html_content):
    return minify(html_content, remove_empty_space=True)


import qrcode
from PIL import Image

def generate_qr_code(data_url, logo_path=None):
    """Generates a QR code for the given URL and optionally overlays a logo."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for logo
        box_size=10,
        border=4,
    )
    qr.add_data(data_url)
    qr.make(fit=True)

    # Generate QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path:
        # Add a logo in the center of the QR code
        logo = Image.open(logo_path)
        # Resize logo to fit within the QR code
        logo_size = min(qr_img.size) // 5  # Adjust the size proportionally
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

        # Calculate position to center the logo
        x_pos = (qr_img.size[0] - logo.size[0]) // 2
        y_pos = (qr_img.size[1] - logo.size[1]) // 2

        # Paste the logo onto the QR code with transparency mask
        qr_img.paste(logo, (x_pos, y_pos), mask=logo if logo.mode == 'RGBA' else None)

    return qr_img



def save_qr_code_image(qr_img, output_path):
    """Saves the QR code image to the specified path."""
    qr_img.save(output_path)


def generate_data_url_from_html(html_content):
    """Generates a data URL from the HTML content."""
    base64_html = base64.b64encode(
        html_content.encode('utf-8')).decode('utf-8')
    return f"data:text/html;base64,{base64_html}"


def main(html_file_path, logo_path=None, output_qr_path='qr_code.png'):
    """Main function to handle the HTML input, minify, generate QR, and save."""
    # Read the HTML file
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Minify the HTML content
    minified_html = minify_html(html_content)

    # Generate the data URL from the HTML
    data_url = generate_data_url_from_html(minified_html)

    # Generate QR code
    qr_img = generate_qr_code(data_url, logo_path)

    # Save the QR code image
    save_qr_code_image(qr_img, output_qr_path)
    print(f"QR code with custom logo saved at {output_qr_path}")


if __name__ == "__main__":
    # You can replace the paths with your specific HTML file and logo file
    html_file = "index.html"  # Path to your HTML file
    logo_file = None  # Optional logo file (can be None if you don't want a logo)

    # Call main function with the file paths
    main(html_file, logo_file)
