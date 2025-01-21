import os
import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

custom_config = r'--oem 3 --psm 6'

def preprocess_image(img_cv):

    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)


    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    binary = cv2.medianBlur(binary, 3)


    plt.imshow(binary, cmap='gray')
    plt.axis('off')
    plt.title('Preprocessed Image')
    plt.show()

    return binary

def save_text_to_file(text, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text)

def process_file(filepath, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    if filepath.lower().endswith('.pdf'):
        print(f"\nProcessing PDF: {filepath}\n")
        # Convert PDF to images
        images = convert_from_path(filepath, dpi=300)
        for i, img in enumerate(images):
            print(f"Processing Page {i + 1}...")

            img_cv = np.array(img)

            binary = preprocess_image(img_cv)
            text = pytesseract.image_to_string(binary, config=custom_config)

            print(f"Extracted Text from Page {i + 1}:")
            print(text)

            output_filename = os.path.join(output_dir, f"page_{i + 1}.txt")
            save_text_to_file(text, output_filename)
            print(f"Text saved to {output_filename}")
    elif filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"\nProcessing Image: {filepath}\n")
        img = Image.open(filepath)
        img_cv = np.array(img)

        binary = preprocess_image(img_cv)
        text = pytesseract.image_to_string(binary, config=custom_config)

        print("Extracted Text:")
        print(text)

        output_filename = os.path.join(output_dir, "image_text.txt")
        save_text_to_file(text, output_filename)
        print(f"Text saved to {output_filename}")
    else:
        print(f"Unsupported file format: {filepath}")


if __name__ == "__main__":
    file_path = input("Enter the file path: ").strip()
    output_directory = "extracted_text"

    if os.path.exists(file_path):
        process_file(file_path, output_directory)
    else:
        print("File not found. Please check the path and try again.")
