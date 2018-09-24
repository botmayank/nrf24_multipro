import cv2

from vision.videosource.camerasrc import CameraSrc

camera = CameraSrc()
while True:
    img = camera.grab_frame()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # qimg = 255 - img
    ret, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find the biggest area
    largest_area = 0
    largest_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largest_area:
            x, y, w, h = cv2.boundingRect(largest_contour)
            print(w, h)
            if w != 1280 and h != 720:
                largest_area = area
                largest_contour = contour

    x, y, w, h = cv2.boundingRect(largest_contour)
    print(x, y, w, h)
    # draw the book contour (in green)
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

    rect = cv2.minAreaRect(largest_contour)
    angle = rect[2]
    print(angle)

    cv2.drawContours(img, largest_contour, -1, 255, 3)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 640, 360)
    cv2.imshow('frame', img)

    k = cv2.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
