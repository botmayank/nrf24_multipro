import os
import shutil

import cv2


def run_camera_and_grab(camera, dir_to_write, n=3):
    """
    :param n: grab every n frames
    :return:
    """
    if os.path.isdir(dir_to_write):
        shutil.rmtree(dir_to_write)
    os.mkdir(dir_to_write)

    total_grabs = 0
    total_frames = 0
    while True:
        ret, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord('g') or total_frames % n == 0:
            cv2.imwrite('%s/%d.png' % (dir_to_write, total_grabs), gray)
            total_grabs += 1
        total_frames += 1
    cv2.destroyAllWindows()


def setup_camera(width=640, height=480, frame_rate=30):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, frame_rate)
    return cap


def setup_video(path):
    cap = cv2.VideoCapture(path)
    return cap


def finalize_camera(camera):
    camera.release()


if __name__ == '__main__':
    # camera = setup_camera(640, 480, 30)
    camera = setup_video("/home/rish/Templates/temp/VID_20180916_165632.mp4")
    run_camera_and_grab(camera, './output/', n=20)
    finalize_camera(camera)
