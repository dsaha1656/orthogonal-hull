import cv2
import numpy as np
import matplotlib.pyplot as plt

input_image = "sample3.jpg"

src = cv2.imread(input_image, 1) 
max_threshold = np.max(src)
min_threshold = np.max(src[src < max_threshold])
src = cv2.imread(input_image, 1) 
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY) 
ret, thresh = cv2.threshold(gray, min_threshold, max_threshold, cv2.THRESH_BINARY)
plt.imshow(gray)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

hull = []
for i in range(len(contours)):
    hull.append(cv2.convexHull(contours[i], False))

drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
color_contours = (0, 255, 0) 
color = (255, 0, 0) 
print("Counture found : ", len(contours))

outer_contour_index = 0
outer_contour_area = 0
for i in range(len(contours)):
    if len(contours[i]) > 4 and (cv2.contourArea(contours[i]) > outer_contour_area):
        outer_contour_area = cv2.contourArea(contours[i])
        outer_contour_index = i
print("Largest contour index : ", outer_contour_index)

outer_contour = contours[outer_contour_index]
cv2.drawContours(drawing, contours, outer_contour_index, color_contours, 1, 8, hierarchy)
cv2.drawContours(drawing, hull, outer_contour_index, color, 1, 8)

hull_points = np.asarray(hull[outer_contour_index])
fig = plt.figure(figsize=(10, 10))
plt.imshow(drawing)

drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
color = (255, 0, 0) 

fig = plt.figure(figsize=(10, 10))
for i in range(len(hull_points)):
    first_point = hull_points[i][0]
    last_point = hull_points[(i+1)%len(hull_points)][0]
    perp_point = (first_point[0], last_point[1])
    plt.plot([first_point[0], perp_point[0]], [first_point[1], perp_point[1]], color)
    plt.plot([perp_point[0], last_point[0]], [perp_point[1], last_point[1]], color)

plt.imshow(drawing)

drawing = np.zeros((thresh.shape[0], thresh.shape[1], 3), np.uint8)
color_contours = (0, 255, 0) 
color = (255, 0, 0) 

for c_index in range(len(contours[outer_contour_index])):
    drawing[contours[outer_contour_index][c_index][0][1], contours[outer_contour_index][c_index][0][0]] = color

fig = plt.figure(figsize=(10, 10))
plt.imshow(drawing)
