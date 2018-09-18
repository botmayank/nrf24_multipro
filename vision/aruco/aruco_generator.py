import cv2
import cv2.aruco as aruco


def draw_aruco(aruco_dict, dir_path, id=0, pixel_size=100):
    img = aruco.drawMarker(aruco_dict, id, pixel_size)
    cv2.imwrite('%s/%d.png' % (dir_path, id), img)


def draw_all_arucos(aruco_dict, dict_length, dir_path, pixel_size=100):
    for id in range(0, dict_length):
        draw_aruco(aruco_dict, dir_path, id, pixel_size)


if __name__ == '__main__':
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    # draw_aruco(aruco_dict, './')
    draw_all_arucos(aruco_dict, 50, './')
