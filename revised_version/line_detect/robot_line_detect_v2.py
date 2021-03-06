import cv2
import numpy as np
import time
import line_detect.geom_util as geom

# 이 부분에 로봇에서 받아온 이미지로 수정해서 추가
datafolder = '/Users/soua/Desktop/Project/RoadImg'
imgpath = datafolder + '/Img_675.jpg'
image = cv2.imread(imgpath)
w, h = image.shape[:2]
# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Define range of white color in HSV
lower_yellow = np.array([20, 40, 240])
upper_yellow = np.array([230, 255, 255])
# Threshold the HSV image
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
# Remove noise
kernel_erode = np.ones((4,4), np.uint8)
eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
kernel_dilate = np.ones((6,6),np.uint8)
dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

conts, max_cont, box = geom.find_main_contour(dilated_mask)

if max_cont is not None:
    M = cv2.moments(max_cont)

    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    print("Centroid of the biggest area: ({}, {})".format(cx, cy))
    cv2.circle(image, (cx, cy), 1, (0, 0, 255))
    # cv2.rectangle(image, )
    p1, p2 = geom.calc_box_vector(box)
    if p1 is not None:
        angle = geom.get_vert_angle(p1, p2, w, h)
        shift = geom.get_horz_shift(p1[0], w)
        print("angle of biggest area: {} degrees".format(angle))

        msg_a = "Angle {0}".format(int(angle))
        msg_s = "Shift {0}".format(int(shift))

        cv2.putText(image, msg_a, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(image, msg_s, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    else:
        print("No angle found")
else:
    print("No Centroid Found")

cv2.drawContours(image, conts, -1, (255, 0, 0), 3)
cv2.imshow('Contour', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

###############################


# imagelist = []
# timelist = []
# for i in range(604, 1722):
#     start_time = time.time()
#     imgpath = datafolder + '/Img_%d.jpg'%i
#     image = cv2.imread(imgpath)
#     w, h = image.shape[:2]
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#
#     lower_yellow = np.array([20, 40, 240])
#     upper_yellow = np.array([230, 255, 255])
#
#     mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
#
#     kernel_erode = np.ones((4, 4), np.uint8)
#     eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
#     kernel_dilate = np.ones((6, 6), np.uint8)
#     dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
#
#     ####요기부터 수정
#     conts, max_cont, box = find_main_contour(dilated_mask)
#     # if cont is not None:
#     #     p1, p2 = geom.calc_box_vector(box)
#     # if p1 is not None:
#     #     angle = geom.get_vert_angle(p1, p2, w, h)
#     #     shift = geom.get_horz_shift(p1[0], w)
#
#     # contours, hierarchy = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
#     # conts = sorted(conts, key=cv2.contourArea, reverse=True)[:1]
#
#     if max_cont is not None:
#         M = cv2.moments(max_cont)
#
#         cx = int(M['m10'] / M['m00'])
#         cy = int(M['m01'] / M['m00'])
#         print("Centroid of the biggest area: ({}, {})".format(cx, cy))
#         p1, p2 = geom.calc_box_vector(box)
#         if p1 is not None:
#             angle = geom.get_vert_angle(p1, p2, w, h)
#             shift = geom.get_horz_shift(p1[0], w)
#             print("angle of biggest area: {} degrees".format(angle))
#
#             msg_a = "Angle {0}".format(int(angle))
#             msg_s = "Shift {0}".format(int(shift))
#
#             cv2.putText(image, msg_a, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
#             cv2.putText(image, msg_s, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
#         else:
#             print("No angle found")
#     else:
#         print("No Centroid Found")
#     ##### 요기까지 수정
#     cv2.drawContours(image, conts, -1, (255, 0, 0), 3)
#
#     imagelist.append(image)
#     timelist.append(time.time()-start_time)
#
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
# out = cv2.VideoWriter('/Users/soua/Desktop/Project/Result/LineTracking/demo20_contour_angle.mp4', fourcc, 20.0, (480,360), True)
#
# for i in range(len(imagelist)):
#     # filename ='../Img_%d.jpg'%i
#     # img = cv2.imread(filename)
#     img = imagelist[i]
#     out.write(img)
#
# out.release()
# cv2.destroyAllWindows()
# print('Avg time for contouring : ', sum(timelist)/len(timelist))
