import cv2


def imshow(img):
    if isinstance(img, str):
        img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
    window_name = "temp"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    try:
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
    except Exception as e:
        print(e)
    cv2.destroyWindow(window_name)
