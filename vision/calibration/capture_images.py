import os
import shutil

import cv2


def run_camera_and_grab(camera, dir_to_write):
    if os.path.isdir(dir_to_write):
        shutil.rmtree(dir_to_write)
    os.mkdir(dir_to_write)

    total_grabs = 0
    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord('g'):
            cv2.imwrite('%s/%d.png' % (dir_to_write, total_grabs), gray)
            total_grabs += 1

    cv2.destroyAllWindows()


def setup_camera(width=640, height=480, frame_rate=30):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, frame_rate)
    return cap


def finalize_camera(camera):
    camera.release()


if __name__ == '__main__':
    camera = setup_camera(640, 480, 30)
    run_camera_and_grab(camera, './output/')
    finalize_camera(camera)
