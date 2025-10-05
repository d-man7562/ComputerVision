import cv2
import numpy as np

class rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
    def width(self):
        return (self.top + self.bottom) / 2

    def height(self):
        return (self.left + self.right) / 2

    def __str__(self):
        return f"Left: {self.left}, Top: {self.top}, Right: {self.right}, Bottom: {self.bottom}"
    def area(self):
        return self.width()*self.height()
    
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    # sort by x (left to right)
    x_sorted = pts[np.argsort(pts[:, 0]), :]

    # left-most two points
    left = x_sorted[:2, :]
    right = x_sorted[2:, :]

    # sort left points by y
    left = left[np.argsort(left[:, 1]), :]
    tl, bl = left

    # sort right points by y
    right = right[np.argsort(right[:, 1]), :]
    tr, br = right

    rect[0] = tl  # top-left
    rect[1] = tr  # top-right
    rect[2] = br  # bottom-right
    rect[3] = bl  # bottom-left

    return rect

# Load the image
image = cv2.imread('C:\\Users\\every\\Downloads\\book.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Edge detection removed because Canny caused 2 pairs of contours to be drawn around each rectangle.
#edges = cv2.Canny(blurred, 75, 200)

#binary threshold makes it easy to find corners
ret, thresh1 = cv2.threshold(blurred,100, 255 ,cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Prepare to draw contours
image_contours = image.copy()
rects = []
# Loop over the contours
print("Shapes detected: ",len(contours))
for contour in contours:
    print("Contour area:", cv2.contourArea(contour))
    # Approximate the contour
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    #print(approx)
    print(len(approx))

    # Perspective transform if the contour has 4 points (likely a card)
    if len(approx) == 4:
        # Draw contours
        cv2.drawContours(image_contours, [approx], -1, (255, 0, 255), 2)

        # Get the points for perspective transform
        pts = approx.reshape(4, 2)
        # # Order the points: top-left, top-right, bottom-right, bottom-left
        rect = order_points(pts)
        print("Ordered points:")
        print(rect)
        left_side = np.linalg.norm(rect[3]-rect[0]) 
        top = np.linalg.norm(rect[1]-rect[0]) 
        right_side = np.linalg.norm(rect[2]-rect[1]) 
        bottom = np.linalg.norm(rect[2]-rect[3])
        rect_obj = rectangle(left_side,top,right_side,bottom)
        rects.append(rect_obj)
       # print(left_side,top,right_side,bottom)
        print("Left:", left_side, "Top:", top, "Right:", right_side, "Bottom:", bottom)
        
        
#I tried using perspective transform but failed and its ok. Error is 12% on width and 6.6% on height
        # # Set desired size and aspect ratio for the cards
        # width = 200
        # height = 300

        # dst = np.array([
        #     [0, 0],
        #     [width - 1, 0],
        #     [width - 1, height - 1],
        #     [0, height - 1]
        # ], dtype="float32")

        # # Compute the perspective transform matrix and apply it
        # M = cv2.getPerspectiveTransform(rect, dst)
        # warp = cv2.warpPerspective(image, M, (width, height))

        # # Show the result
        # cv2.imshow('Warped Card', warp)
        cv2.waitKey(0)
# Known real-world sizes (in cm)
paper_width_cm = 21.5
paper_height_cm = 27.8
book_width_cm = 8.0    # Just for comparison
book_height_cm = 10.6

# Use the first rectangle (paper) as reference
paper_rect = rects[0]
book_rect = rects[1]

# Get pixel dimensions
paper_pixel_width = paper_rect.width()
paper_pixel_height = paper_rect.height()

# Calculate pixel-per-cm ratio
pixel_per_cm_width = paper_pixel_width / paper_width_cm
pixel_per_cm_height = paper_pixel_height / paper_height_cm

# Get book's pixel size
book_pixel_width = book_rect.width()
book_pixel_height = book_rect.height()

# Convert book pixel dimensions to real-world cm
estimated_book_width_cm = book_pixel_width / pixel_per_cm_width
estimated_book_height_cm = book_pixel_height / pixel_per_cm_height

# Print comparison
print("Estimated Book Dimensions:")
print(f"Width: {estimated_book_width_cm:.2f} cm (Expected: {book_width_cm} cm)")
print(f"Height: {estimated_book_height_cm:.2f} cm (Expected: {book_height_cm} cm)")

# Optional: calculate error percentages
width_error = abs(estimated_book_width_cm - book_width_cm) / book_width_cm * 100
height_error = abs(estimated_book_height_cm - book_height_cm) / book_height_cm * 100

print(f"Width Error: {width_error:.2f}%")
print(f"Height Error: {height_error:.2f}%")
# Show the image with detected contours
#cv2.imshow('Image with Contours', image_contours)
cv2.imshow('threshold image',thresh1)
# cv2.imshow('Image', image)
cv2.imshow('Image with Contours', image_contours)


cv2.waitKey(0)
cv2.destroyAllWindows()
