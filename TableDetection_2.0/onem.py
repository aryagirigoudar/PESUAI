import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import pandas as pd
import random as r

image_path = '1.png'
image = cv2.imread(image_path)
bitnot = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

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
length = np.array(image).shape[1] // 100
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1))




horizontal_detect = cv2.erode(inverted_image, horizontal_kernel, iterations=3)
hor_line = cv2.dilate(horizontal_detect, horizontal_kernel, iterations=3)
plotting = plt.imshow(horizontal_detect,cmap='gray')
plt.show()


vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, length))
vertical_detect = cv2.erode(inverted_image, vertical_kernel, iterations=3)
ver_lines = cv2.dilate(vertical_detect, vertical_kernel, iterations=3)
show = plt.imshow(vertical_detect,cmap='gray')
plt.show()


# Combine horizontal and vertical lines
final = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
combine = cv2.addWeighted(ver_lines, 0.5, hor_line, 0.5, 0.0)
combine = cv2.erode(~combine, final, iterations=2)
_, combine = cv2.threshold(combine, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

image_shape = image.shape[:2]
#resize
combine_resized = cv2.resize(combine, (image_shape[1], image_shape[0]))
combine_resized_color = cv2.cvtColor(combine_resized, cv2.COLOR_GRAY2BGR)
# Perform bitwise XOR operation to highlight cells
convert_xor = cv2.bitwise_xor(image, combine_resized_color)
inverse = cv2.bitwise_not(convert_xor)


# output= plt.imshow(inverse,cmap='gray')
# plt.show()
plt.imshow(inverse, cmap='gray')
plt.title('Highlighted Cells')
plt.axis('off')
plt.show()


# Convert the combine_resized_color to grayscale
combine_resized_gray = combine_resized
_, combine_binary = cv2.threshold(combine_resized_gray, 128, 255, cv2.THRESH_BINARY)

cont, _ = cv2.findContours(combine_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
def get_boxes(num, method="left-to-right"):
    invert = False
    if method == "right-to-left" or method == "bottom-to-top":
        invert = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        flag = 1
    boxes = [cv2.boundingRect(c) for c in num]
    sorted_boxes = sorted(zip(boxes, num), key=lambda b: b[0][1], reverse=invert)
    num, sorted_boxes = zip(*sorted_boxes)
    return num, sorted_boxes
cont, boxes = get_boxes(cont, method="top-to-bottom")








final_box = []

test = 0
for c in cont:
    x, y, width, height = c
    top_left = (x, y)
    top_right = (x + width, y)
    bottom_right = (x + width, y + height)
    bottom_left = (x, y + height)
    rectangle_points = [top_left, top_right, bottom_right, bottom_left]
    rectangle_points = np.asarray(rectangle_points)
    x, y, w, h = cv2.boundingRect(rectangle_points)
    temp = r.choice(range(255))
    if w < 500 and h < 500:
        rectangle_img = cv2.rectangle(image, (x, y), (x + w, y + h), (r.choice(range(255)), temp, r.choice(range(255))), 2)
        final_box.append([x, y, w, h])

graph = plt.imshow(rectangle_img, cmap='gray')
plt.show()



dim = [boxes[i][3] for i in range(len(boxes))]
avg = np.mean(dim)
hor = []
ver = []
for i in range(len(boxes)):
    if(i==0):
        ver.append(boxes[i])
        last=boxes[i]
    else:
        if np.all((boxes[i][1]<=last[1]+avg/2)):
            ver.append(boxes[i])
            last=boxes[i]            
            if(i==len(boxes)-1):
                hor.append(ver)
        else:
            hor.append(ver)
            ver=[]
            last = boxes[i]
            ver.append(boxes[i])
total = 0
for i in range(len(hor)):
    total = len(hor[i])
    if total > total:
        total = total

mid = []

for sublist in hor:
    for box in sublist:
        if len(sublist) > 0:
            k = (box[0] + box[2]) / 2
            midpoint = k.tolist()
            mid.append(midpoint)

mid = np.array(mid)
mid.sort()

order = []
for i in range(len(hor)):
    arrange = [[] for _ in range(total)]
    for j in range(len(hor[i])):
        sub = abs(mid[i] - (hor[i][j][0] + hor[i][j][2] / 4))
        idx = np.argmin(sub)
        arrange[idx].append(hor[i][j])
    order.append(arrange)
    
extract = []


for i in range(len(order)-1):
    for j in range(len(order[i])-1):
        inside = ''
        if len(order[i][j]) == 0:
            extract.append(' ')
        else:
            for k in range(len(order[i][j])):
                x = order[i][j][k][0][0][0]
                y = order[i][j][k][1][0][0]
                width = order[i][j][k][2][0][1]
                height = order[i][j][k][3][0][0]

                final_extract = bitnot[x:x+width, y:y+height]
                final_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                get_border = cv2.copyMakeBorder(final_extract, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=[0, 255])
                resize = cv2.resize(get_border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                dil = cv2.dilate(resize, final_kernel, iterations=1)
                ero = cv2.erode(dil, final_kernel, iterations=2)
                ocr = pytesseract.image_to_string(ero)
                # plt.imshow(ero, cmap='gray')
                # plt.title('Eroded Image')
                # plt.axis('off')
                # plt.show()®

                if len(ocr) == 0:
                    ocr = pytesseract.image_to_string(ero, config='--psm 3')
                inside = inside + " " + ocr
            extract.append(inside)
for text in extract:
    print(text)





