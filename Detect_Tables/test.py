
# import pandas as pd
# import io
# import cv2
# import numpy as np

# # # Read image
# # img = cv2.imread('test.png')

# # # Convert image to grayscale
# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # # Apply adaptive thresholding
# # thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
# #             cv2.THRESH_BINARY_INV,11,2)

# # # Find contours in the thresholded image
# # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # # Loop through the contours to find the table
# # for cnt in contours:
# #     # Find the area of the contour
# #     area = cv2.contourArea(cnt)

# #     # Find the perimeter of the contour
# #     perimeter = cv2.arcLength(cnt,True)

# #     # Find the number of corners of the contour
# #     corners = cv2.approxPolyDP(cnt,0.01*perimeter,True)

# #     # If the area of the contour is greater than a threshold and it has 4 corners, it is likely to be a table
# #     if area > 5000 and len(corners) == 4:
# #         # Draw the contour on the original image
# #         cv2.drawContours(img,[cnt],0,(0,0,255),2)

# # # Show the image with the detected table
# # cv2.imshow('Detected Table', img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()





# # import pytesseract
# # import pandas as pd

# # # Load the image
# img = cv2.imread('test2.png')

# # # Convert the image to grayscale
# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # # Threshold the grayscale image to convert it to a binary image
# # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# # # Find the contours in the binary image
# # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # # Find the contour with the largest area, which should be the table
# # max_area = 0
# # max_contour = None
# # for contour in contours:
# #     area = cv2.contourArea(contour)
# #     if area > max_area:
# #         max_area = area
# #         max_contour = contour

# # # Extract the table region from the image
# # x, y, w, h = cv2.boundingRect(max_contour)
# # table_img = img[y:y+h, x:x+w]

# # # Convert the table image to grayscale and apply adaptive thresholding
# # gray_table = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
# # thresh_table = cv2.adaptiveThreshold(gray_table, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

# # # Use Pytesseract to extract text from the table image
# # table_text = pytesseract.image_to_string(thresh_table)

# # # Create window with name 'image'
# # cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# # # Show image in window
# # cv2.imshow('image', table_text)



# # cv2.waitKey(0)
# # cv2.destroyAllWindows()

# # # Define the separator
# # separator = '|'

# # # Perform OCR on the image and get the text
# # text = pytesseract.image_to_string(thresh_table)

# # # Replace newlines with the separator
# # text = text.replace('\n', separator)

# # # Print the text
# # print(text)


# import cv2
# import pytesseract

# # Load the image


# # Convert to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Apply adaptive thresholding to binarize the image
# thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 20)

# # Find contours in the image
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # Draw bounding boxes around cells and crop them
# cell_imgs = []
# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     if w > 20 and h > 20:  # Filter out small contours which are not cells
#         cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw bounding box
#         cell_img = img[y:y+h, x:x+w]  # Crop cell image
#         cell_imgs.append(cell_img)

# st = ""
# # Loop through the cell images and extract text using OCR
# for cell_img in cell_imgs:
#     cell_text = pytesseract.image_to_string(cell_img, config='--psm 6')
#     print(cell_text)



import tabula

df = tabula.read_pdf("my2.pdf", pages=0)

tabula.convert_into("my2.pdf", "my2.csv", output_format="csv", pages='all')
print(df)