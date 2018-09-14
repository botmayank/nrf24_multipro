import cv2
import cv2.aruco as aruco
import numpy as np


def run_camera_and_detect(cap, camera_matrix, dist_matrix):
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = aruco.detectMarkers(gray, dictionary)

        if ids is not None and len(ids) > 0:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.015, camera_matrix, dist_matrix)

            aruco.drawAxis(gray, camera_matrix, dist_matrix, rvec[0], tvec[0], 0.02)
            aruco.drawDetectedMarkers(gray, corners, ids)
            stride = abs(corners[0][0][0][0] - corners[0][0][1][0])
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(gray, "Length: %f" % stride, (0, 50), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

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
    camera_matrix = np.array([[7.2751531880861648e+02, 0., 3.3573062809603971e+02],
                              [0., 7.2902821773214896e+02, 2.2879353141911656e+02],
                              [0., 0., 1.]])
    dist_matrix = np.array([4.8412257817011632e-02, -1.2834569362402684e-01,
                            -2.6153996114361634e-03, 5.9434689889416460e-03,
                            -1.5490960578187754e+00])

    return cap, camera_matrix, dist_matrix


def finalize_camera(cap):
    cap.release()


if __name__ == '__main__':
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

    camera, camera_matrix, dist_matrix = setup_camera(640, 480, 30)
    run_camera_and_detect(camera, camera_matrix, dist_matrix)
    finalize_camera(camera)
