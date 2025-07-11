import numpy as np
import cv2

def compute_radii(coins):
    radii = []
    for rounded_thingy in coins[0, :]:
        radii.append(rounded_thingy[2])
    return radii

def av_pix(img, circles, size):
    av_value = []
    for rounded_thingy in circles[0, :]:
        col = np.mean(
            img[rounded_thingy[1]-size:rounded_thingy[1]+size,
                rounded_thingy[0]-size:rounded_thingy[0]+size]
        )
        av_value.append(col)
    return av_value

# Load image (grayscale for processing, color for display)
img = cv2.imread('coins.jpeg', cv2.IMREAD_GRAYSCALE)
original_img = cv2.imread('coins.jpeg', 1)

# Blur to reduce noise
img = cv2.GaussianBlur(img, (5, 5), 0)

# Detect circles
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 460,
                           param1=47, param2=49, minRadius=80, maxRadius=120)

# If no circles detected
if circles is None:
    print("No circles found.")
    exit()

# Round and draw circles
circles = np.uint16(np.around(circles))
for idx, i in enumerate(circles[0, :]):
    cv2.circle(original_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.circle(original_img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.putText(original_img, str(idx), (i[0], i[1]),
                cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 0, 0), 2)

# Measure radii and light intensity
radii = compute_radii(circles)
light_intensity = av_pix(img, circles, 20)

# Classify coin values
values = []
for a, b in zip(light_intensity, radii):
    if a >= 75 and b > 105:
        values.append(2)
    else:
        values.append(1)

# Annotate coin values
for idx, i in enumerate(circles[0, :]):
    cv2.putText(original_img, f"{values[idx]}$", (i[0], i[1]+50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Annotate total
cv2.putText(original_img, "Estimated Total Value: $" + str(sum(values)),
            (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 2)

# Display image
cv2.imshow("Detected Coins", original_img)
cv2.waitKey(0)
cv2.destroyAllWindows()