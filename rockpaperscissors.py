import random
import cv2
import time
import cvzone
import pygame
import numpy as np
from cvzone.HandTrackingModule import HandDetector

pygame.init()

w, h = 1280, 720
wind = pygame.display.set_mode((w, h))
pygame.display.set_caption("LapTop.studios")

fps = 30
clock = pygame.time.Clock()

clicked = False

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(detectionCon=0.8, maxHands=1)
score = [0, 0]
stargame = False
stateresult = False
randomnumb = 0
timer = 0
player = 0
imgai = cv2.imread("../RESURSES/1.png", cv2.IMREAD_UNCHANGED)

stop = True
while stop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = False
            pygame.quit()

    imgbg = cv2.imread("../RESURSES/BG.png")
    san, img = cap.read()
    img = cv2.flip(img, 1)
    imgscaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgscaled = imgscaled[:, 80:480]

    hands = detector.findHands(imgscaled, draw=True)

    if stargame:

        imgbg[234:654, 795:1195] = imgscaled

        if stateresult is False:
            timer = time.time() - initialTime
            cv2.putText(imgbg, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateresult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 1, 1, 1, 1]:
                        player = 2
                    elif fingers == [1, 0, 0, 0, 0] or fingers == [0, 0, 0, 0, 0] or fingers == [0, 0, 0, 0, 1]\
                            or fingers == [0, 0, 0, 1, 1] :
                        player = 1
                    elif fingers == [1, 1, 1, 0, 0]:
                        player = 3

                    randomnumb = random.randint(1, 3)
                    imgai = cv2.imread(f"../RESURSES/{randomnumb}.png", cv2.IMREAD_UNCHANGED)
                    imgbg = cvzone.overlayPNG(imgbg, imgai, (149, 310))

                    if (player == 1 and randomnumb == 2) or (player == 2 and randomnumb == 3) or (player == 3 and randomnumb == 1):
                        score[0] += 1
                    if (player == 1 and randomnumb == 3) or (player == 2 and randomnumb == 1) or (player == 3 and randomnumb == 2):
                        score[1] += 1
                    else:
                        pass

    if stateresult:
        imgbg = cvzone.overlayPNG(imgbg, imgai, (149, 310))

    key = cv2.waitKey(1)

    if key == 27:
        cv2.destroyAllWindows()
        break
    if key == ord("s"):
        stateresult = False
        stargame = True
        initialTime = time.time()
        player = 0

    if cv2.getWindowProperty("imgscaled", cv2.WND_PROP_VISIBLE) < 1:
        pass

    cv2.putText(imgbg, str(score[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (100, 0, 100), 4)
    cv2.putText(imgbg, str(score[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (100, 0, 100), 4)

    #cv2.imshow("imgbg", imgbg)

    imgrgb = cv2.cvtColor(imgbg, cv2.COLOR_BGR2RGB)
    imgrgb = np.rot90(imgrgb)
    frame = pygame.surfarray.make_surface(imgrgb).convert()
    frame = pygame.transform.flip(frame, True, False)

    wind.fill((255, 255, 255))
    wind.blit(frame, (0, 0))

    qwerty = pygame.draw.rect(wind, (1, 1, 1), (556, 636, 168, 68), border_radius=3)
    ABC = pygame.draw.rect(wind, (250, 250, 250), (560, 640, 160, 60), border_radius=3)
    font2 = pygame.font.Font('../RESURSES/Cuprum Bold Italic.ttf', 50)
    text2 = font2.render("Старт", True, (255, 0, 255))
    pos = pygame.mouse.get_pos()
    wind.blit(text2, (565, 640))

    if ABC.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1 and clicked is False:
            clicked = True
            initialTime = time.time()
            stateresult = False
            stargame = True
            player = 0

        if pygame.mouse.get_pressed()[0] == 0:
            clicked = False

    cv2.waitKey(1)

    pygame.display.update()
    clock.tick(fps)

