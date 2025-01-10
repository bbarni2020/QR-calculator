import base64
import qrcode
from PIL import Image
import io
import sys
import os
from htmlmin import minify  # Import the minify function from the htmlmin module


def minify_html(html_content):
    return minify(html_content, remove_empty_space=True)


def generate_qr_code(data_url, logo_path=None):
    """Generates QR code from the data URL and adds logo (optional)."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_url)
    qr.make(fit=True)

    # Generate QR code image
    qr_img = qr.make_image(fill="black", back_color="white")

    if logo_path:
        # Overlay logo in the center of the QR code
        logo = Image.open(logo_path)
        logo = logo.resize(
            (50, 50))  # Resize logo to fit in the QR code center
        qr_img.paste(logo, (int((qr_img.size[0] - logo.size[0]) / 2),
                            int((qr_img.size[1] - logo.size[1]) / 2)))

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
