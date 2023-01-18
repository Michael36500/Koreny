import cv2

# Load image (as BGR for later drawing the circle)
image = cv2.imread('elipseIMG.png', cv2.IMREAD_COLOR)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Get rid of possible JPG artifacts (when do people learn to use PNG?...)
_, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Downsize image (by factor 4) to speed up morphological operations
gray = cv2.resize(gray, dsize=(0, 0), fx=0.25, fy=0.25)

# Morphological Closing: Get rid of the hole
gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    
# Morphological opening: Get rid of the stuff at the top of the circle
# gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (121, 121)))

# Resize image to original size
gray = cv2.resize(gray, dsize=(image.shape[1], image.shape[0]))

# Find contours (only most external)
# cnts, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Draw found contour(s) in input image
# image = cv2.drawContours(image, cnts, -1, (0, 0, 255), 2)

cv2.imwrite('elipsoided.png', gray)