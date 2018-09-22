import math

import cv2
import cv2.aruco as aruco
import numpy as np

from vision.videosource.camerasrc import CameraSrc


class ArucoFinder:

    def __init__(self):
        self.aruco_size_in_cm = 6
        self.aruco_marker_id = 17
        self.not_detected = 0
        self.frame_count = 0
        self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.camerasrc = CameraSrc()
        self.tracker = cv2.TrackerKCF_create()
        self.prev_frame = None
        self.prev_detected = False
        self.prev_box = None
        np.set_printoptions(precision=0)

    def __del__(self):
        del self.camerasrc

    def run_camera_and_detect(self, show_window=False):
        frame = self.camerasrc.grab_frame()
        self.frame_count += 1
        if frame is None:
            return None
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
        # detector_params.minOtsuStdDev = 10

        # detector_params.perspectiveRemoveIgnoredMarginPerCell = 0.4

        # kinda increases by 4-5% but only when I set it very high
        # detector_params.errorCorrectionRate = 1

        # detector_params.maxErroneousBitsInBorderRate = 1

        corners, ids, rejected_corners = aruco.detectMarkers(gray, self.dictionary, parameters=detector_params,
                                                             cameraMatrix=self.camerasrc.camera_matrix)
        # show rejected corners
        '''
        print('rejected: ', len(rejected_corners))
        for rejected_corner in rejected_corners:
            cv2.rectangle(gray, tuple(rejected_corner[:, 0].astype(int).tolist()[0]),
                          tuple(rejected_corner[:, 2].astype(int).tolist()[0]),
                          (255, 255, 255), thickness=4)
        '''

        # track if not detected
        if ids is None or self.aruco_marker_id not in ids:
            self.not_detected += 1
            if self.prev_detected:
                x, y = np.min(self.prev_box[:, 0]), np.min(self.prev_box[:, 1])
                w, h = np.max(self.prev_box[:, 0]) - np.min(self.prev_box[:, 0]), \
                       np.max(self.prev_box[:, 1]) - np.min(self.prev_box[:, 1])
                self.tracker = cv2.TrackerKCF_create()
                padding = 20
                self.tracker.init(self.prev_frame, (x - padding / 2, y - padding / 2, w + padding, h + padding))
                self.prev_detected = False

            ok, bbox = self.tracker.update(gray)
            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(gray, p1, p2, (255, 255, 255), 2, 1)

        # else detect since there's at least of one marker our interest
        elif len(ids) > 0:
            # get the first array element with id == aruco_marker_id
            marker_index = np.array(np.where(np.squeeze(ids) == self.aruco_marker_id))[0, 0]
            # rvec and tvec contain relative pose of marker wrt camera
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, self.aruco_size_in_cm,
                                                            self.camerasrc.camera_matrix, self.camerasrc.dist_matrix)
            rvec = rvec[marker_index]
            tvec = tvec[marker_index]
            rmat, _ = cv2.Rodrigues(rvec)
            aruco.drawAxis(gray, self.camerasrc.camera_matrix, self.camerasrc.dist_matrix, rvec, tvec,
                           self.aruco_size_in_cm / 2)
            aruco.drawDetectedMarkers(gray, corners, ids)

            self.prev_box = np.squeeze(corners[marker_index])
            self.text(gray, 'tvec: %s' % np.squeeze(tvec), 1)
            x = 180 + math.atan2(rmat[1, 0], rmat[0, 0]) * 180 / math.pi
            self.text(gray, 'angle: %s' % x, 2)
            self.prev_detected = True

        if show_window:
            cv2.waitKey(1)
            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 640, 360)
            cv2.imshow('frame', gray)
            k = cv2.waitKey(1)
            if k == ord('q'):
                exit(-1)
                return 1

        self.prev_frame = gray
        return 10

    def text(self, frame, text, id):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (320, 180 + id * 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


if __name__ == '__main__':
    aruco_finder = ArucoFinder()
    while True:
        # start = time.time() * 1000.0
        if aruco_finder.run_camera_and_detect(True) is None:
            break
        # print('time taken: ', (time.time() * 1000.0 - start))
        if cv2.waitKey(1) & 0xFF == ord('h'):
            break
    print('detections rate:', (1 - aruco_finder.not_detected / aruco_finder.frame_count) * 100.0)
    del aruco_finder
