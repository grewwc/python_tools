import cv2
import numpy as np
import sys

# from python_tools.opencv import imshow


fname = "C:/Users/User/Desktop/images/person/messi.jpeg"


def print_mouse_position(fname):
    img = cv2.imread(fname)

    def get_mouse_position(event, x, y, flags, params):
        print(x, y)

    cv2.namedWindow("position", cv2.WINDOW_NORMAL)

    cv2.setMouseCallback('position', get_mouse_position)

    while 1:
        cv2.imshow('position', img)
        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    assert len(sys.argv) == 2, "type the filename please"
    fname = sys.argv[1]
    print_mouse_position(fname)
