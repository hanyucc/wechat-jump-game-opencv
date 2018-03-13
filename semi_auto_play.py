import cv2
import os
import time


mouse_x = mouse_y = -1


def get_mouse_click(event, x, y, flags, param):
    global mouse_x, mouse_y

    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_x = x
        mouse_y = y


def get_screenshot():
    os.system('adb exec-out screencap -p > screenshot.png')
    return cv2.imread('screenshot.png')


def move_player(curr_x, curr_y, next_x, next_y):
    dist = 3 ** 0.5 * abs(next_y - curr_y) + abs(next_x - curr_x)
    dist = int(dist ** 0.9 * 1.52)
    os.system('adb shell input touchscreen swipe 200 200 200 200 ' + str(dist))
    

def main():
    global mouse_x, mouse_y

    while True:
        time.sleep(1.5)

        mouse_x = mouse_y = -1

        img = get_screenshot()
        img = cv2.resize(img, (1080, 1920))

        cv2.namedWindow('select locations', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('select locations', 270, 480)
        cv2.setMouseCallback('select locations', get_mouse_click)

        curr_x = curr_y = next_x = next_y = -1

        while True:
            cv2.imshow('select locations', img)
            if cv2.waitKey(20) & 0xFF == 27:
                break
            if mouse_x != -1:
                if curr_x != -1:
                    next_x = mouse_x
                    next_y = mouse_y
                    break
                else:
                    curr_x = mouse_x
                    curr_y = mouse_y
                    mouse_x = -1
                    mouse_y = -1

        cv2.destroyAllWindows()

        if curr_x == -1 or next_x == -1:
            continue

        move_player(curr_x, curr_y, next_x, next_y)


if __name__ == '__main__':
    main()
