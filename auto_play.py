import cv2
import os
import numpy as np
import time
import math
import random


def get_screenshot():
    os.system('adb exec-out screencap -p > screenshot.png')
    return cv2.imread('screenshot.png')


def move_player(curr_x, curr_y, next_x, next_y):
    dist = 3 ** 0.5 * abs(next_y - curr_y) + abs(next_x - curr_x)
    dist = int(dist ** 0.9 * 1.13)
    os.system('adb shell input touchscreen swipe 200 200 200 200 ' + str(dist))


def find_player(img):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100,
                               param1=50, param2=30, minRadius=40, maxRadius=60)
    return circles[0][0]


def length(line):
    return ((line[0] - line[2]) ** 2 + (line[1] - line[3]) ** 2) ** 0.5


def angle(line):
    return math.atan2(abs(line[1] - line[3]), abs(line[0] - line[2]))


def similar(s1, s2, s3):
    if abs(s1[0] - s2[0]) < 30 and abs(s2[0] - s3[0]) < 30 and abs(s1[0] - s3[0]) < 30:
        if abs(s1[1] - s2[1]) < 30 and abs(s2[1] - s3[1]) < 30 and abs(s1[1] - s3[1]) < 30:
            return True
    return False


def canny_rectangle_detector(img):
    edges = cv2.Canny(img, 20, 80)
    edges = cv2.dilate(edges, None)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 200, minLineLength=200, maxLineGap=20)
    possible_lines = list()

    if lines is None:
        return []

    for line in lines:
        if length(line[0]) > 500 or (angle(line[0]) - np.pi / 4) > 0.1:
            continue
        possible_lines.append(line[0])
        cv2.line(edges, (line[0][0], line[0][1]), (line[0][2], line[0][3]), 128, 3)

    if len(possible_lines) == 0:
        return []

    possible_lines.sort(key=lambda x: x[1])

    return [[possible_lines[0][0], possible_lines[0][3]]]


def find_square(img):
    img = cv2.resize(img, None, fx=1, fy=3 ** 0.5)

    squares = list()

    squares.extend(canny_rectangle_detector(img[:, :, 0]))
    squares.extend(canny_rectangle_detector(img[:, :, 1]))
    squares.extend(canny_rectangle_detector(img[:, :, 2]))
    squares.extend(canny_rectangle_detector(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))

    squares.sort(key=lambda x: x[1])

    if len(squares) == 3:
        if similar(squares[0], squares[1], squares[2]) or similar(squares[0], squares[1], squares[3]) or similar(squares[0], squares[2], squares[3]):
            return [squares[0][0], squares[0][1] / 3 ** 0.5]
        elif similar(squares[1], squares[2], squares[3]):
            return [squares[1][0], squares[1][1] / 3 ** 0.5]
    elif len(squares) != 0:
        return [squares[0][0], squares[0][1] / 3 ** 0.5]

    return None


def hough_circle_detector(img):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100,
                               param1=30, param2=30, minRadius=60, maxRadius=0)

    return [] if circles is None else [circles[0][0]]


def find_circle(img):
    img = cv2.resize(img, None, fx=1, fy=3 ** 0.5)
    img = cv2.GaussianBlur(img, (11, 11), 0)

    circles = list()

    circles.extend(hough_circle_detector(img[:, :, 0]))
    circles.extend(hough_circle_detector(img[:, :, 1]))
    circles.extend(hough_circle_detector(img[:, :, 2]))
    circles.extend(hough_circle_detector(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))

    if len(circles) == 4:
        if similar(circles[0], circles[1], circles[2]) or similar(circles[0], circles[1], circles[3]) or similar(circles[0], circles[2], circles[3]):
            return [circles[0][0], circles[0][1] / 3 ** 0.5]
        elif similar(circles[1], circles[2], circles[3]):
            return [circles[1][0], circles[1][1] / 3 ** 0.5]
    elif len(circles) != 0:
        return [circles[0][0], circles[0][1] / 3 ** 0.5]

    return None


def main():
    while True:
        time.sleep(1.5 + 1.5 * random.random())

        img = get_screenshot()
        img = cv2.resize(img, None, fx=1.5, fy=1.5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)

        coords = find_player(blur[400:2000, :])  # use grayscale image here
        coords = coords.astype('int')

        coords[1] += 660
        curr_x, curr_y = coords[0], coords[1]

        next_x = next_y = -1

        square = find_square(img[1000:coords[1] - 100, :])  # use bgr image here
        if square is not None:
            next_x = int(square[0])
            next_y = int(square[1] + 1000)
            print('square detected at (%d, %d)\n' % (next_x, next_y))
            move_player(curr_x, curr_y, next_x, next_y)
            continue

        circle = find_circle(img[1000:coords[1] - 50, :])
        if circle is not None:
            next_x = int(circle[0])
            next_y = int(circle[1] + 1000)
            print('circle detected at (%d, %d)\n' % (next_x, next_y))
            move_player(curr_x, curr_y, next_x, next_y)
            continue

        if next_x == -1 or next_y == -1:
            print('nothing detected\n')
            break


if __name__ == '__main__':
    main()
