import cv2
import cv2.aruco as aruco
import numpy as np


class ArucoFinder:

    def __init__(self, width=640, height=480, frame_rate=30):
        self.not_detected = 0
        self.frame_count = 0
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.camera, self.camera_matrix, self.dist_matrix = self.setup_camera(width, height, frame_rate)
        self.tracker = cv2.TrackerKCF_create()
        self.prev_frame = None
        self.prev_detected = False
        self.prev_bb = None

    def __del__(self):
        self.finalize_camera(self.camera)

    def run_camera_and_detect(self, show_window=False):
        ret, frame = self.camera.read()
        self.frame_count += 1
        if frame is None:
            return -2
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        b = 0
        c = 127
        gray = cv2.addWeighted(gray, 1. + c / 127., gray, 0, b - c)
        gray = cv2.bilateralFilter(gray, 9, 75, 75)

        detector_params = aruco.DetectorParameters_create()
        # adaptiveThreshWinSizeStep : changing this has almost no effect
        # detector_params.adaptiveThreshWinSizeStep = 3

        # adaptiveThreshWinSizeMax: increasing size of adaptiveThreshWinSizeMax to 103 added 5-8% increase in detection
        # detector_params.adaptiveThreshWinSizeMax = 103

        # adaptiveThreshConstant has almost no effect
        # detector_params.adaptiveThreshConstant = 4

        # polygonalApproxAccuracyRate seems to be doing fine with the default
        # detector_params.polygonalApproxAccuracyRate = 0.08

        # need to understand minOtsuStdDev
        detector_params.minOtsuStdDev = 10

        detector_params.perspectiveRemoveIgnoredMarginPerCell = 0.4

        # kinda increases by 4-5% but only when I set it very high
        # detector_params.errorCorrectionRate = 1

        # detector_params.maxErroneousBitsInBorderRate = 1

        corners, ids, rejected_corners = aruco.detectMarkers(gray, self.dictionary, parameters=detector_params,
                                                             cameraMatrix=self.camera_matrix)

        # show rejected corners
        '''
        print('rejected: ', len(rejected_corners))
        for rejected_corner in rejected_corners:
            cv2.rectangle(gray, tuple(rejected_corner[:, 0].astype(int).tolist()[0]),
                          tuple(rejected_corner[:, 2].astype(int).tolist()[0]),
                          (255, 255, 255), thickness=4)
        '''

        dist = -1
        if ids is None or 17 not in ids:
            self.not_detected += 1
            if self.prev_detected:
                a = self.prev_bb[:, 0].astype(int).tolist()[0]
                b = self.prev_bb[:, 2].astype(int).tolist()[0]
                self.tracker = cv2.TrackerKCF_create()
                print((a[0], a[1], abs(b[0] - a[0]), abs(b[1] - a[1])))
                ok = self.tracker.init(self.prev_frame, (a[0] - 50, a[1] - 50, 100, 100))
                print('ok=', ok)
                self.prev_detected = False

            ok, bbox = self.tracker.update(gray)
            if ok:
                print("=--------------ok")
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (255, 255, 255), 2, 1)
            else:
                print('not ok')
        elif len(ids) > 0:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.07, self.camera_matrix, self.dist_matrix)
            self.prev_bb = corners[0]
            self.prev_detected = True
            aruco.drawAxis(gray, self.camera_matrix, self.dist_matrix, rvec[0], tvec[0], 0.3)
            aruco.drawDetectedMarkers(gray, corners, ids)
            p1 = corners[0][0][0]
            p2 = corners[0][0][1]
            dist = np.linalg.norm(p1 - p2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray, "Length: %f" % dist, (0, 50), font, 0.5, (255, 255, 255), 3, cv2.LINE_AA)

        if show_window:  # and ids is None:
            cv2.waitKey(1)
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 640, 360)
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return 1
            # cv2.imwrite('not_detected-%d.png' % frame_count, gray)

        self.prev_frame = gray
        return dist

    def setup_camera(self, width=640, height=480, frame_rate=30):
        camera = cv2.VideoCapture("../../media/syma_aruco_4x4_17_short_2.mp4")
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
        # start = time.time() * 1000.0
        if aruco_finder.run_camera_and_detect(True) == -2:
            break
        # print('time taken: ', (time.time() * 1000.0 - start))
        if cv2.waitKey(1) & 0xFF == ord('h'):
            break
    print('detections rate:', (1 - aruco_finder.not_detected / aruco_finder.frame_count) * 100.0)
    del aruco_finder
