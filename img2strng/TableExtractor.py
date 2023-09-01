import cv2
import matplotlib.pyplot as plt
import pytesseract

# Load the preprocessed image
image_path = '1.png'
preprocessed_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Perform OCR to extract text from the entire image
extracted_text = pytesseract.image_to_string(preprocessed_image)

# Print or process the extracted text
print(extracted_text)
