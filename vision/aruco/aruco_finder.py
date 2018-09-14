import cv2
import cv2.aruco as aruco
import numpy as np


def run_camera_and_detect(cap, camera_matrix, dist_matrix):
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(gray, dictionary)

        if ids is not None and len(ids) > 0:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, camera_matrix, dist_matrix)

            aruco.drawAxis(gray, camera_matrix, dist_matrix, rvec[0], tvec[0], 0.1)
            aruco.drawDetectedMarkers(gray, corners, ids)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def setup_camera(width=640, height=480, frame_rate=30):
    '''
    :return: todo ideally return this as a class
    '''
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, frame_rate)

    # todo read these values from the camera calibration
    camera_matrix = np.array([[500., 0., 320.],
                              [0., 500., 240.],
                              [0., 0., 1.]])
    dist_matrix = np.array([0., 0., 0., 0., 0.])

    return cap, camera_matrix, dist_matrix


def finalize_camera(cap):
    cap.release()


if __name__ == '__main__':
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    camera, camera_matrix, dist_matrix = setup_camera(640, 480, 30)
    run_camera_and_detect(camera, camera_matrix, dist_matrix)
    finalize_camera(camera)
