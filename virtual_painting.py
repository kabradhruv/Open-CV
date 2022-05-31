import cv2 as c
import numpy as np

cap = c.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 500)

# defining colours
# Yellow,purple,pink
myColor = [
    [1, 145, 128, 255, 110, 255],
    [0, 179, 113, 255, 105, 255],
    [156, 179, 64, 219, 79, 255]
]
mycolorValue = [
    [0, 230, 255],
    [206, 60, 108],
    [96, 47, 255]
]

mypoints = [
]


def getContours(img):
    x, y, w, h = 0, 0, 0, 0
    contours, hierarchy = c.findContours(img, c.RETR_EXTERNAL, c.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = c.contourArea(cnt)
        if area < 500:
            # c.drawContours(imgResult, cnt, -1, (255, 0, 0),thickness=c.FILLED
            peri = c.arcLength(cnt, True)
            approx = c.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = c.boundingRect(approx)

    return x + w // 2, y


# defining main function
def findcolor(image, mycolor, mycolorValue):
    imagehsv = c.cvtColor(image, c.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in mycolor:
        h_min = color[0]
        h_max = color[1]
        s_min = color[2]
        s_max = color[3]
        v_min = color[4]
        v_max = color[5]
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = c.inRange(imagehsv, lower, upper)
        # c.imshow(str(color[0]), mask)
        x, y = getContours(mask)
        c.circle(imgResult, (x, y), 20, mycolorValue[count], c.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints


def draw_on_canvas(mypoints, mycolorValue):
    for point in mypoints:
        c.circle(imgResult, (point[0], point[1]), 20, mycolorValue[point[2]], c.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findcolor(img, myColor, mycolorValue)
    if len(newPoints) != 0:
        for newp in newPoints:
            mypoints.append(newp)

    if len(mypoints) != 0:
        draw_on_canvas(mypoints, mycolorValue)

    c.imshow("live video", img)
    c.imshow("Video after Contour", imgResult)
    if c.waitKey(10) & 0xFF == ord('q'):
        break
c.destroyAllWindows()
    