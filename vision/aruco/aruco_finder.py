import time

import cv2
import cv2.aruco as aruco
import numpy as np


class ArucoFinder:

    def __init__(self, width=640, height=480, frame_rate=30):
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.camera, self.camera_matrix, self.dist_matrix = self.setup_camera(width, height, frame_rate)

    def __del__(self):
        self.finalize_camera(self.camera)

    def run_camera_and_detect(self, show_window=False):
        ret, frame = self.camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(gray, self.dictionary)

        dist = -1
        if ids is not None and len(ids) > 0:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.07, self.camera_matrix, self.dist_matrix)
            aruco.drawAxis(gray, self.camera_matrix, self.dist_matrix, rvec[0], tvec[0], 0.3)
            aruco.drawDetectedMarkers(gray, corners, ids)
            p1 = corners[0][0][0]
            p2 = corners[0][0][1]
            dist = np.linalg.norm(p1 - p2)
            print(dist)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray, "Length: %f" % dist, (0, 50), font, 0.5, (255, 255, 255), 3, cv2.LINE_AA)

        if show_window:
            cv2.waitKey(1)
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 640, 360)
            cv2.imshow('frame', gray)

        return dist

    def setup_camera(self, width=640, height=480, frame_rate=30):
        camera = cv2.VideoCapture("../../media/syma_aruco_4x4.mp4")
        print(camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # camera.set(cv2.CAP_PROP_FPS, frame_rate)

        # todo read these values from the camera calibration
        camera_matrix = np.array([[989.43041893, 0., 643.65628421],
                                  [0., 992.17579024, 342.38060762],
                                  [0., 0., 1.]])
        dist_matrix = np.array([2.13212094e-01, -1.78417926e+00, -2.79719436e-03, -2.82407212e-03, 8.10910900e+00])

        return camera, camera_matrix, dist_matrix

    def finalize_camera(self, camera):
        camera.release()


if __name__ == '__main__':
    aruco_finder = ArucoFinder()
    while True:
        start = time.time() * 1000.0
        aruco_finder.run_camera_and_detect(True)
        print('time taken: ', (time.time() * 1000.0 - start))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    del aruco_finder
