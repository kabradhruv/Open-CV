import cv2 as c
import numpy as np
import pyttsx3

# defining speak function
engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)


def speak(audio, rate=150):
    engine.setProperty('rate', rate)
    engine.say(audio)
    engine.runAndWait()


speak("this is an open cv program which lets you identify the colour number for white parts", 160)
speak("adjust the hue,sat,val accordingly and press Q then",160)
speak("Then type the colour name and it will automatically be saved in the colour.txt",160)
speak("wait a minute program is starting", 150)

cap = c.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 320)
cap.set(10, 500)


# defining empty function
def empty(a):
    pass


# creating trackbars
c.namedWindow("TrackBars")
c.resizeWindow("TrackBars", 640, 240)
c.createTrackbar("Hue min", "TrackBars", 0, 179, empty)
c.createTrackbar("Hue max", "TrackBars", 145, 179, empty)
c.createTrackbar("sat min", "TrackBars", 128, 255, empty)
c.createTrackbar("sat max", "TrackBars", 255, 255, empty)
c.createTrackbar("val min", "TrackBars", 110, 255, empty)
c.createTrackbar("val max", "TrackBars", 255, 255, empty)

while True:
    success, img = cap.read()
    # code for colore picker
    imghsv = c.cvtColor(img, c.COLOR_BGR2HSV)
    h_min = c.getTrackbarPos("Hue min", "TrackBars")
    h_max = c.getTrackbarPos("Hue max", "TrackBars")
    s_min = c.getTrackbarPos("sat min", "TrackBars")
    s_max = c.getTrackbarPos("sat max", "TrackBars")
    v_min = c.getTrackbarPos("val min", "TrackBars")
    v_max = c.getTrackbarPos("val max", "TrackBars")
    color_numbers = [h_min, h_max, s_min, s_max, v_min, v_max]
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = c.inRange(imghsv, lower, upper)
    imgresult = c.bitwise_and(img, img, mask=mask)
    c.imshow("video live", img)
    # c.imshow("my image", imghsv)
    c.imshow("Mask", mask)
    # c.imshow("results", imgresult)
    if c.waitKey(10) == ord('q'):
        break
    # code for color picker ended

c.destroyAllWindows()
speak("Do you want to save this colour")
decision=str(input("Yes or no:>"))
if decision=="Yes" or decision=="yes" or decision=="y":
    speak("please type Colour name", 180)
    colorname = str(input("type the name of the colour :>"))

    try:
        with open("colour.txt", "a") as p:
            var = (f"\n\nColour name = {colorname}\n"
                   f"colour number = {color_numbers}")
            p.write(var)
        speak(f"Your colour name {colorname} and your colour numbers {color_numbers} are succesfully appended to "
              f"colour.txt file", 250)
        print(
            f"Your colour name {colorname} and your colour numbers {color_numbers} are succesfully appended to colour.txt file")
    except Exception as e:
        print(
            f"Your colour name {colorname} and your colour numbers {color_numbers}\nare not appended to colour.txt file due to\n{e}")
        speak(
            f"Your colour name {colorname} and your colour numbers {color_numbers}\nare not appended to colour.txt file due to\n{e}")
else:
    speak("thank you.Come back again")

