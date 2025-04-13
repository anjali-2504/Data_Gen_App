import numpy as np
from PIL import Image
import cv2

im_gray = np.array(Image.open(r"C:\Users\abhis\Desktop\scrib.jpg").convert('L'))
im_bw = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


img1 = cv2.imread(r"tomorrow_gt.jpg")
img2 = cv2.imread(r"C:\Users\abhis\Desktop\scrib.jpg")

# resize img2 to the same size as img1
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# convert img1 to grayscale
gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# threshold the grayscale image
ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

# bitwise-and mask and original image
masked_img = cv2.bitwise_and(img1, img1, mask=mask)

# bitwise-and inverse mask and second image
masked_img_inv = cv2.bitwise_and(img2, img2, mask=cv2.bitwise_not(mask))

# add masked and inverse masked images together
final_img = cv2.add(masked_img, masked_img_inv)

cv2.imshow('final', final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()