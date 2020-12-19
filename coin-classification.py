# imports the relevant libraries; numpy for computations and openCV for machine perception
import numpy as np
import cv2

def compute_radii (coins):
     radii = []
     for rounded_thingy in circles[0,:]: # Coudn't think of another name. No, really.
         radii.append(rounded_thingy[2])
     return radii

def av_pix (img, circle, size):
    av_value = []
    for rounded_thingy in circles[0,:]:
        col = np.mean(img[rounded_thingy[1]-size:rounded_thingy[1]+size, rounded_thingy[0]-size:rounded_thingy[0]+size])
        av_value.append(col)
        return av_value

# read the image and render it black and white (reducing colours makes the application easier); also, it starts to detec
# circles everywhere for some reason
img = cv2.imread('coins.jpeg', cv2.IMREAD_GRAYSCALE)
# original image
original_img = cv2.imread('coins.jpeg', 1)
# adds some blur to reduce clarity; else it detects circles everywhere
img = cv2.GaussianBlur(img, (5, 5), 0)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 460,
                           param1=47, param2=49, minRadius=80, maxRadius= 120)

# Rounds up the coordinates
circles = np.uint16(np.around(circles))
count = 0
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(original_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(original_img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.putText(original_img, str(count) , (i[0], i[1]), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0, 0, 0), 2)
    count += 1

# print(circles)
radii = compute_radii(circles)
print(radii)

# print brightness values
light_intensity = av_pix(img, circles, 20)
print(light_intensity)

values = []
for a,b in zip(light_intensity, radii):
    if (a>=75 & b >105):
        values.append(2)
    print(values)
    count_2 = 0
    for i in circles[0,:]:
        cv2.putText(original_img, str(values[count_2]) + "$", (i[0],i[1]), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (0,0,0), 2 )
        count_2 += 1
    cv2.putText(original_img, "Estimated Total Value: " + "$" + str(sum(values)), (200,100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.3, 255 )


# Commented out; these three lines of code are simply there to generate the window to show the code works
cv2.imshow("Img", original_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
