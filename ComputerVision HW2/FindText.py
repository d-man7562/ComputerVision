from PIL import Image
import cv2
import pytesseract
import numpy as np
custom_config = r'--oem 3 --psm 6'
str = ''
total_chars = 70
def draw_boxes(data, img):
    # Loop over each word detected
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:  # Confidence threshold to avoid false positives
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, data['text'][i], (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    return img
def order_points(pts):
    """ Orders the points in top-left, top-right, bottom-right, bottom-left order """
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left

    return rect

def warp_region(image, pts, output_size=(300, 300)):
    rect = order_points(pts)
    dst = np.array([
        [0, 0],
        [output_size[0] - 1, 0],
        [output_size[0] - 1, output_size[1] - 1],
        [0, output_size[1] - 1]
    ], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, output_size)
    return warped
# Simple image to string
img =cv2.imread("C:\\Users\\every\\Downloads\\text.jpg")
img1 =cv2.imread("C:\\Users\\every\\Downloads\\sign1.jpg")
img2 =cv2.imread("C:\\Users\\every\\Downloads\\sign2.jpg")
img3 =cv2.imread("C:\\Users\\every\\Downloads\\sign3.jpg")
imgs = [img,img1,img2,img3]
for im in imgs:
#if im is img2:
# OCR on the warped image
   # blur = cv2.GaussianBlur(im,(1,1),1)
    #blur = cv2.medianBlur(blur, 1)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #denoised = cv2.fastNlMeansDenoising(blur, h=10)
    _, thresh = cv2.threshold(gray, 100,255, cv2.THRESH_BINARY_INV)
    #thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)


    str +=(pytesseract.image_to_string(cleaned, config='--psm 6'))
    data = pytesseract.image_to_data(cleaned, output_type=pytesseract.Output.DICT, config=custom_config)   
    #print(data['text'])    
    draw_boxes(data,im) 
    #print("Detected text:", text.strip())
    #cv2.imshow("denoised",denoised)

    cv2.imshow("gray img", cleaned)
    #cv2.imshow("denoised img", denoised)
    cv2.imshow("Warped Sign", im)
    cv2.waitKey(0)
print(f"{total_chars/len(str)} = accuracy ")
