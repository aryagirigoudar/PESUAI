import cv2
import numpy as np
import pytesseract
import mysql.connector

# Constants
IMAGE_PATH = '1/11.png'
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'dbp'
}

# Step 1: Table Detection
def detect_table(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    table_contour = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            table_contour = approx
            break

    return table_contour

# Step 2: Cell Recognition and Text Extraction
def recognize_table(image, table_contour):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [table_contour], -1, 255, -1)
    masked_image = cv2.bitwise_and(gray, gray, mask=mask)

    cells = pytesseract.image_to_string(masked_image, config='--psm 6')

    return cells

# Step 3: Database Connection
db_connection = mysql.connector.connect(**DATABASE_CONFIG)
db_cursor = db_connection.cursor()

# Step 4: Table Detection, Cell Recognition, and Text Extraction
image = cv2.imread(IMAGE_PATH)
table_contour = detect_table(image)

if table_contour is not None:
    table_cells = recognize_table(image, table_contour)
    
    # Step 5: Store Table Data in Database
    table_data = table_cells.split('\n')
    for row in table_data:
        columns = row.split('\t')
        if len(columns) >= 3:  # Check if the columns list has at least 3 elements
            query = "INSERT INTO table_data (column1, column2, column3) VALUES (%s, %s, %s)"
            values = (columns[0], columns[1], columns[2])  # Adjust column indices as per your table structure
            db_cursor.execute(query, values)
            db_connection.commit()
        else:
            print("Invalid row: ", row)
    
    print("Table data stored in the database.")
else:
    print("No table found in the image.")

# Step 6: Closing Database Connection
db_cursor.close()
db_connection.close()
