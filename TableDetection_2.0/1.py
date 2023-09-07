import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract

# Load the image
image_path = '1.png'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Otsu's thresholding
_, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Invert the thresholded image
inverted_image = 255 - thresholded_image

# Display the inverted image using Matplotlib
plt.imshow(inverted_image, cmap='gray')
plt.title('Inverted Thresholded Image')
plt.axis('off')
plt.show()

# Calculate the length for the horizontal kernel
length = image.shape[1] // 100
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1))

# Detect horizontal lines
horizontal_detect = cv2.erode(inverted_image, horizontal_kernel, iterations=3)
hor_line = cv2.dilate(horizontal_detect, horizontal_kernel, iterations=3)
plt.imshow(horizontal_detect, cmap='gray')
plt.title('Horizontal Lines')
plt.axis('off')
plt.show()

# Calculate the length for the vertical kernel
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, length))

# Detect vertical lines
vertical_detect = cv2.erode(inverted_image, vertical_kernel, iterations=3)
ver_lines = cv2.dilate(vertical_detect, vertical_kernel, iterations=3)
plt.imshow(vertical_detect, cmap='gray')
plt.title('Vertical Lines')
plt.axis('off')
plt.show()

# Combine horizontal and vertical lines
final = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
combine = cv2.addWeighted(ver_lines, 0.5, hor_line, 0.5, 0.0)
combine = cv2.erode(~combine, final, iterations=2)
_, combine = cv2.threshold(combine, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Highlight cells in the original image
combine_resized = cv2.resize(combine, (image.shape[1], image.shape[0]))
combine_resized_color = cv2.cvtColor(combine_resized, cv2.COLOR_GRAY2BGR)
highlighted_cells = cv2.bitwise_xor(image, combine_resized_color)
highlighted_cells = cv2.bitwise_not(highlighted_cells)
plt.imshow(highlighted_cells, cmap='gray')
plt.title('Highlighted Cells')
plt.axis('off')
plt.show()

# Find contours of cells
_, contours, _ = cv2.findContours(combine, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extract text from each cell
extracted_text = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w < 500 and h < 500:
        cell = inverted_image[y:y+h, x:x+w]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cell = cv2.copyMakeBorder(cell, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=[0, 100])
        cell = cv2.resize(cell, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        cell = cv2.dilate(cell, kernel, iterations=1)
        cell = cv2.erode(cell, kernel, iterations=2)
        text = pytesseract.image_to_string(cell, config='--psm 6')
        extracted_text.append(text.strip())

# Print the extracted text
for text in extracted_text:
    print(text)
